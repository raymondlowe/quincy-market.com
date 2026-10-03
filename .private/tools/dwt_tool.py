#!/usr/bin/env python3
"""
DWT Tool - Standalone CLI for applying DWT templates to HTML files

Combines core DWT processing with batch and single-file CLI functionality.
Supports single files, folders (recursive or not), dry runs, and various output modes.



Changelog:
- v1.0.0 - 2024-06-15: Initial version combining core DWT processing and CLI handling
- v1.1.0 - 2025-09-18: Added marker comment at end of html
- v1.2.0 - 2025-09-18: Fixed dry-run mode to perform full validation (editable region checks) and accurate error counting without modifying files
"""
version = "v1.2.0"
import os
import sys
import argparse
from pathlib import Path
from typing import List, Optional
import glob
from datetime import datetime
import re

# Debug mode
debug = False

def set_debug_mode(enabled: bool):
    """Set debug mode globally."""
    global debug
    debug = enabled

def debug_print(message: str):
    if debug:
        print(f"DEBUG: {message}", file=sys.stderr)

def normalize_output_lines(lines: List[str]) -> List[str]:
    """Ensure all lines have consistent newline endings for output."""
    normalized = []
    for line in lines:
        # Remove any existing line endings
        clean_line = line.rstrip('\r\n')
        # Add consistent \n ending
        normalized.append(clean_line + '\n')
    
    debug_print(f"Normalized {len(normalized)} output lines")
    return normalized

def write_lines_to_file(filename: str, lines: List[str]) -> None:
    """Write lines to file with consistent newline handling."""
    normalized_lines = normalize_output_lines(lines)
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        for line in normalized_lines:
            f.write(line)
    debug_print(f"Wrote {len(normalized_lines)} lines to {filename}")

def load_file(filename: str) -> List[str]:
    """Load file and normalize line endings to ensure consistent newlines."""
    with open(filename, 'r', encoding='utf-8-sig') as file:
        content = file.read()
    
    # Normalize line endings: convert \r\n and \r to \n
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    # Split into lines and ensure each line ends with \n (except possibly the last)
    lines = content.split('\n')
    
    # Convert back to list with proper newlines
    normalized_lines = []
    for i, line in enumerate(lines):
        if i == len(lines) - 1 and line == '':
            # Skip empty last line that results from split if file ends with \n
            continue
        elif i == len(lines) - 1:
            # Last line - preserve whether it had a newline or not in original
            if content.endswith('\n'):
                normalized_lines.append(line + '\n')
            else:
                normalized_lines.append(line + '\n')  # Always add newline for consistency
        else:
            # All other lines should have newlines
            normalized_lines.append(line + '\n')
    
    debug_print(f"Loaded {len(normalized_lines)} lines from {filename}")
    return normalized_lines

def search_file_for_string(lines: List[str], search_string: str, starting_from: int = 0) -> int:
    debug_print(f"Searching for '{search_string}' starting from line {starting_from}")
    for i, line in enumerate(lines[starting_from:], start=starting_from):
        if search_string in line:
            debug_print(f"Found '{search_string}' at line {i}")
            return i
    return -1

def find_region_0_html(html_lines: List[str]) -> tuple[int, int]:
    """Find Region 0 in HTML: from start until BeginTemplate line (inclusive)"""
    for i, line in enumerate(html_lines):
        if '<!-- #BeginTemplate' in line:
            debug_print(f"HTML Region 0: lines 0 to {i + 1} (inclusive)")
            return 0, i + 1  # Include the BeginTemplate line
    debug_print("HTML Region 0: No BeginTemplate found, returning 0,0")
    return 0, 0  # No template found

def find_region_0_dwt(dwt_lines: List[str]) -> tuple[int, int]:
    """Find Region 0 in DWT: from start until <head tag (exclusive)"""
    for i, line in enumerate(dwt_lines):
        if '<head' in line.lower():
            debug_print(f"DWT Region 0: lines 0 to {i} (exclusive)")
            return 0, i  # Exclude the <head line
    debug_print("DWT Region 0: No <head> found, returning 0,0")
    return 0, 0  # No head found

def apply_dwt_to_file(filename: str, timestamp: Optional[str] = None) -> List[str]:
    if not os.path.isfile(filename):
        print(f"Error: File not found: {filename}")
        sys.exit(1)

    # Validate file has .html extension
    if not filename.lower().endswith(('.html', '.htm')):
        print(f"Error: File must have .html or .htm extension: {filename}")
        sys.exit(1)

    relative_path = os.path.dirname(filename)

    # Load and validate HTML file
    try:
        html_lines = load_file(filename) 
    except UnicodeDecodeError as e:
        print(f"Error: Unable to read file {filename}: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to load file {filename}: {e}")
        sys.exit(1)
    
    if not html_lines:
        print(f"Error: File is empty: {filename}")
        sys.exit(1) 

    # Validate that the html is in the expected format, it has a begintemplate line after the <html but before the <head , exit if it does not
    html_tag_line_number = search_file_for_string(html_lines, '<html')
    begintemplate_tag_line_number = search_file_for_string(html_lines, '<!-- #BeginTemplate "')
    head_tag_line_number = search_file_for_string(html_lines, '<head')
    body_tag_line_number = search_file_for_string(html_lines, '<body')

    # only if these four variables are in the expected order, do we proceed
    if not (0 <= html_tag_line_number < begintemplate_tag_line_number < head_tag_line_number < body_tag_line_number):
        print(f"HTML file {filename} is not in the expected format.")
        # should be, but actually was
        print(f"html_tag_line_number: {html_tag_line_number}")
        print(f"begintemplate_tag_line_number: {begintemplate_tag_line_number}")
        print(f"head_tag_line_number: {head_tag_line_number}")
        print(f"body_tag_line_number: {body_tag_line_number}")
        sys.exit(1)

    # html files must have begin template and a matching number of begin editable and end editable tags
    if begintemplate_tag_line_number == -1:
        print(f"HTML file {filename} does not contain a <!-- #BeginTemplate \"...\" --> tag.")
        sys.exit(1)
    count_editable_begin = sum(1 for line in html_lines if '<!-- #BeginEditable' in line)
    count_editable_end = sum(1 for line in html_lines if '<!-- #EndEditable -->' in line)
    if count_editable_begin != count_editable_end:
        print(f"HTML file {filename} has mismatched #BeginEditable and #EndEditable tags.")
        print(f"#BeginEditable count: {count_editable_begin}, #EndEditable count: {count_editable_end}")
        sys.exit(1)
  
    debug_print(f"begintemplate_tag_line_number: {begintemplate_tag_line_number}")
    if begintemplate_tag_line_number == -1:
        print(f"DWT line not found in {filename}")
        sys.exit(1)

    # Extract the DWT file name from the line
    dwt_file_line = html_lines[begintemplate_tag_line_number]
    try:
        dwt_file = dwt_file_line.split('"')[1]
    except (IndexError, AttributeError):
        print(f"Error: Malformed BeginTemplate line in {filename}: {dwt_file_line.strip()}")
        sys.exit(1)
    
    if not dwt_file:
        print(f"Error: Empty template filename in BeginTemplate line: {dwt_file_line.strip()}")
        sys.exit(1)

    # Load the DWT file from relative path
    dwt_file = os.path.join(relative_path, dwt_file)
    if not os.path.isfile(dwt_file):
        print(f"Error: DWT template file not found: {dwt_file}")
        sys.exit(1)
    
    try:
        dwt_lines = load_file(dwt_file)
    except UnicodeDecodeError as e:
        print(f"Error: Unable to read DWT template file {dwt_file}: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to load DWT template file {dwt_file}: {e}")
        sys.exit(1)
    
    if not dwt_lines:
        print(f"Error: DWT template file is empty: {dwt_file}")
        sys.exit(1)

    # make new_html_lines by copying the entire dwt file
    new_html_lines = dwt_lines.copy()

    # adjust relative paths
    dwt_folder = os.path.dirname(dwt_file)
    html_folder = os.path.dirname(filename)
    debug_print(f"dwt_folder: {dwt_folder}, html_folder: {html_folder}")
    
    # Normalize paths to prevent path traversal issues
    try:
        dwt_folder = os.path.normpath(dwt_folder)
        html_folder = os.path.normpath(html_folder)
    except Exception as e:
        print(f"Error: Invalid path structure: {e}")
        sys.exit(1)
        
    if dwt_folder == html_folder:
        relative_adjustment = ""
    else:   
        dwt_folder_parts = dwt_folder.split(os.sep) if dwt_folder else []
        html_folder_parts = html_folder.split(os.sep) if html_folder else []
        
        # find common parts
        common_parts = 0
        for dwt_part, html_part in zip(dwt_folder_parts, html_folder_parts):
            if dwt_part == html_part:
                common_parts += 1
            else:
                break
        # calculate the adjustment
        up_moves = len(html_folder_parts) - common_parts
        down_moves = dwt_folder_parts[common_parts:]
        
        # Validate that we don't have too many up moves (potential security issue)
        if up_moves > 10:  # Reasonable limit
            print(f"Error: Too many directory levels to traverse ({up_moves}). This may indicate a path issue.")
            sys.exit(1)
            
        relative_adjustment = os.sep.join(['..'] * up_moves + down_moves)
        if relative_adjustment:
            relative_adjustment += os.sep
        # Normalize the path to clean up any redundant separators
        relative_adjustment = os.path.normpath(relative_adjustment + "dummy").replace("dummy", "")
        if relative_adjustment and not relative_adjustment.endswith(os.sep):
            relative_adjustment += os.sep
    debug_print(f"relative_adjustment: '{relative_adjustment}'")

    # Apply relative path adjustments to the DWT content before processing
    if relative_adjustment:
        adjusted_dwt_lines = []
        for line in new_html_lines:
            # Adjust src attributes
            if 'src="' in line and not line.strip().startswith('<!--'):
                # Find src="path" and adjust relative paths (not absolute URLs)
                line = re.sub(r'src="(?!https?://)(?!/)([^"]+)"', 
                            f'src="{relative_adjustment}\\1"', line)
            # Adjust href attributes  
            if 'href="' in line and not line.strip().startswith('<!--'):
                # Find href="path" and adjust relative paths (not absolute URLs)
                line = re.sub(r'href="(?!https?://)(?!/)([^"]+)"', 
                            f'href="{relative_adjustment}\\1"', line)
            adjusted_dwt_lines.append(line)
        new_html_lines = adjusted_dwt_lines

    # identify the editable regions and make a dictionary where the key is the region name and the content is the list of lines in the HTML file
    editable_regions = {}
    current_region_name = None
    current_region_lines = []
    in_editable_region = False
    for line in html_lines:
        if '<!-- #BeginEditable' in line:
            if in_editable_region:
                print(f"Error: Nested BeginEditable found at line: {line.strip()}")
                sys.exit(1)
            in_editable_region = True
            try:
                current_region_name = line.split('"')[1]
            except (IndexError, AttributeError):
                print(f"Error: Malformed BeginEditable line: {line.strip()}")
                sys.exit(1)
            if current_region_name in editable_regions:
                print(f"Error: Duplicate editable region name '{current_region_name}' found")
                sys.exit(1)
            current_region_lines = []
        elif '<!-- #EndEditable -->' in line:
            if not in_editable_region:
                print(f"Error: EndEditable found without matching BeginEditable: {line.strip()}")
                sys.exit(1)
            in_editable_region = False
            if current_region_name:
                editable_regions[current_region_name] = current_region_lines
                current_region_name = None
                current_region_lines = []
        elif in_editable_region and current_region_name:
            current_region_lines.append(line)
    
    if in_editable_region:
        print(f"Error: Unclosed editable region '{current_region_name}' found")
        sys.exit(1)
        
    debug_print(f"Editable regions found: {list(editable_regions.keys())}")
        
    # now do a similar thing in the new_html_lines, make a dictionary where the key is the region name and the values is a list with first and last line number of the region
    dwt_regions = {}
    current_region_name = None
    in_editable_region = False
    for i, line in enumerate(new_html_lines):
        if '<!-- #BeginEditable' in line:
            if in_editable_region:
                print(f"Error: Nested BeginEditable found in DWT template at line {i}: {line.strip()}")
                sys.exit(1)
            in_editable_region = True
            try:
                current_region_name = line.split('"')[1]
            except (IndexError, AttributeError):
                print(f"Error: Malformed BeginEditable line in DWT template: {line.strip()}")
                sys.exit(1)
            if current_region_name in dwt_regions:
                print(f"Error: Duplicate editable region name '{current_region_name}' in DWT template")
                sys.exit(1)
            dwt_regions[current_region_name] = [i, None]  # start line number
        elif '<!-- #EndEditable -->' in line and in_editable_region and current_region_name:
            in_editable_region = False
            dwt_regions[current_region_name][1] = i  # end line number
            current_region_name = None
    
    if in_editable_region:
        print(f"Error: Unclosed editable region '{current_region_name}' in DWT template")
        sys.exit(1)
        
    debug_print(f"DWT regions found: {dwt_regions}")
    
    # Validate that HTML and DWT template have matching editable regions
    html_region_names = set(editable_regions.keys())
    dwt_region_names = set(dwt_regions.keys())
    
    if html_region_names != dwt_region_names:
        missing_in_html = dwt_region_names - html_region_names
        missing_in_dwt = html_region_names - dwt_region_names
        error_msg = "Error: Editable region mismatch between HTML and DWT template:"
        if missing_in_html:
            error_msg += f"\n  Missing in HTML: {', '.join(missing_in_html)}"
        if missing_in_dwt:
            error_msg += f"\n  Missing in DWT: {', '.join(missing_in_dwt)}"
        print(error_msg)
        sys.exit(1)
    debug_print(f"DWT regions found: {dwt_regions}")

    #now, working backwards from the right of the dwt regions dictionary, replace the lines in new_html_lines with the corresponding lines from editable_regions
    for region_name in reversed(list(dwt_regions.keys())):
        if region_name in editable_regions:
            start_line, end_line = dwt_regions[region_name]
            debug_print(f"Replacing region '{region_name}' from line {start_line} to {end_line} in new_html_lines")
            # replace the lines in new_html_lines from start_line+1 to end_line-1 with the lines from editable_regions[region_name]
            new_html_lines = (new_html_lines[:start_line + 1] +
                              editable_regions[region_name] +
                              new_html_lines[end_line:])
        else:
            debug_print(f"Region '{region_name}' not found in editable_regions, skipping replacement.")   

    # if the new_html_lines has no #EndTemplate line then insert it after the closing </body> and before the closing </html>
    endtemplate_line_number = search_file_for_string(new_html_lines, '<!-- #EndTemplate -->')
    if endtemplate_line_number == -1:
        body_close_line_number = search_file_for_string(new_html_lines, '</body>')
        html_close_line_number = search_file_for_string(new_html_lines, '</html>')
        if body_close_line_number != -1 and html_close_line_number != -1 and body_close_line_number < html_close_line_number:
            new_html_lines.insert(html_close_line_number, '<!-- #EndTemplate -->\n')
            debug_print(f"Inserted <!-- #EndTemplate --> at line {html_close_line_number}")
        else:
            print(f"Could not find </body> and </html> tags in the expected order to insert <!-- #EndTemplate -->")
            sys.exit(1)

    # Insert the BeginTemplate marker from the HTML into the output built from the DWT
    begin_template_present = any('<!-- #BeginTemplate' in line for line in new_html_lines)
    if not begin_template_present and begintemplate_tag_line_number != -1:
        begin_template_line = html_lines[begintemplate_tag_line_number]
        head_index = search_file_for_string(new_html_lines, '<head')
        insert_index = head_index if head_index != -1 else 0
        new_html_lines.insert(insert_index, begin_template_line)
        debug_print(f"Inserted <!-- #BeginTemplate --> at line {insert_index}")
    else:
        debug_print("BeginTemplate marker already present or not found in HTML; no insertion performed")

    # Keep template markers (like EndTemplate) in final output
    debug_print("Ensuring template markers are present in final output")

    # Add update comment if timestamp provided
    if timestamp:
        comment = f"\n<!-- updated by dwt_tool.py {version} on {timestamp} -->\n"
        new_html_lines.append(comment)
        debug_print(f"Added update comment: {comment.strip()}")

    return new_html_lines

class DWTUIProcessor:
    """Main class for handling DWT template processing with CLI options."""
    
    def __init__(self, dry_run: bool = False, verbose: bool = False, start_time: Optional[str] = None):
        self.dry_run = dry_run
        self.verbose = verbose
        self.start_time = start_time
        self.processed_files = []
        self.skipped_files = []
        self.error_files = []
        
    def log(self, message: str, level: str = "INFO"):
        """Log messages with timestamp."""
        if self.verbose or level in ["ERROR", "SUCCESS"]:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {level}: {message}")
    
    def find_html_files(self, path: str, recursive: bool = True) -> List[str]:
        """Find all HTML files in the given path."""
        html_files = []
        path_obj = Path(path)
        
        if path_obj.is_file():
            if path.lower().endswith(('.html', '.htm')):
                html_files.append(str(path_obj))
            else:
                self.log(f"File {path} is not an HTML file", "WARNING")
        elif path_obj.is_dir():
            if recursive:
                # Find HTML files recursively
                pattern = "**/*.html"
                pattern_htm = "**/*.htm"
                html_files.extend([str(p) for p in path_obj.glob(pattern)])
                html_files.extend([str(p) for p in path_obj.glob(pattern_htm)])
            else:
                # Find HTML files only in current directory
                pattern = "*.html"
                pattern_htm = "*.htm"
                html_files.extend([str(p) for p in path_obj.glob(pattern)])
                html_files.extend([str(p) for p in path_obj.glob(pattern_htm)])
        else:
            self.log(f"Path {path} does not exist", "ERROR")
            return []
            
        # Remove duplicates and sort
        html_files = sorted(list(set(html_files)))
        self.log(f"Found {len(html_files)} HTML files", "INFO")
        
        return html_files
    
    def has_dwt_template_marker(self, file_path: str) -> bool:
        """Check if HTML file has DWT template marker."""
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                content = f.read()
                return '<!-- #BeginTemplate' in content
        except Exception as e:
            self.log(f"Error reading {file_path}: {e}", "ERROR")
            return False
    
    def process_single_file(self, input_file: str, output_file: Optional[str] = None, 
                          overwrite: bool = False, print_to_stdout: bool = True) -> bool:
        """Process a single HTML file."""
        try:
            # Check if file has DWT template marker
            if not self.has_dwt_template_marker(input_file):
                self.log(f"Skipping {input_file} - no DWT template marker found", "WARNING")
                self.skipped_files.append(input_file)
                return False
            
            if self.dry_run:
                self.log(f"DRY RUN: Validating {input_file}...", "INFO")
                try:
                    # Perform full validation without output
                    _ = apply_dwt_to_file(input_file, self.start_time)
                    self.log(f"DRY RUN: Validation passed for {input_file}", "INFO")
                    self.processed_files.append(input_file)
                    return True
                except SystemExit:
                    self.log(f"DRY RUN: Validation failed (mismatch/errors) for {input_file}", "ERROR")
                    self.error_files.append(input_file)
                    return False
                except Exception as e:
                    self.log(f"DRY RUN: Unexpected validation error for {input_file}: {e}", "ERROR")
                    self.error_files.append(input_file)
                    return False
            else:
                # Original non-dry-run logic
                self.log(f"Processing {input_file}...", "INFO")
                new_html_lines = apply_dwt_to_file(input_file, self.start_time)
                
                # Handle output
                if output_file:
                    # Output to specific file
                    output_dir = os.path.dirname(output_file)
                    if output_dir:  # Only create directory if there's a path component
                        os.makedirs(output_dir, exist_ok=True)
                    write_lines_to_file(output_file, new_html_lines)
                    self.log(f"Output written to {output_file}", "SUCCESS")
                elif overwrite:
                    # Overwrite original file
                    write_lines_to_file(input_file, new_html_lines)
                    self.log(f"File overwritten: {input_file}", "SUCCESS")
                elif print_to_stdout:
                    # Output to stdout
                    normalized_lines = normalize_output_lines(new_html_lines)
                    for line in normalized_lines:
                        print(line, end='')
                
                self.processed_files.append(input_file)
                return True
            
        except SystemExit:
            # apply_dwt_to_file calls sys.exit() on errors (non-dry-run)
            self.log(f"Error processing {input_file}", "ERROR")
            self.error_files.append(input_file)
            return False
        except Exception as e:
            self.log(f"Unexpected error processing {input_file}: {e}", "ERROR")
            self.error_files.append(input_file)
            return False
    
    def process_folder(self, input_folder: str, output_folder: Optional[str] = None, 
                      recursive: bool = True, overwrite: bool = False) -> None:
        """Process all HTML files in a folder."""
        html_files = self.find_html_files(input_folder, recursive)
        
        if not html_files:
            self.log("No HTML files found to process", "WARNING")
            return
        
        self.log(f"Starting batch processing of {len(html_files)} files...", "INFO")
        
        for i, html_file in enumerate(html_files, 1):
            self.log(f"Processing file {i}/{len(html_files)}: {os.path.basename(html_file)}", "INFO")
            
            output_file = None
            if output_folder:
                # Calculate relative path from input folder to maintain structure
                input_path = Path(input_folder)
                file_path = Path(html_file)
                try:
                    rel_path = file_path.relative_to(input_path)
                    output_file = str(Path(output_folder) / rel_path)
                except ValueError:
                    # File is not relative to input folder (shouldn't happen)
                    output_file = str(Path(output_folder) / file_path.name)
            
            success = self.process_single_file(html_file, output_file, overwrite, print_to_stdout=False)
            
            # In batch mode, just continue processing - don't prompt for continuation
            # Errors and skips will be logged and reported in the final summary
    
    def print_summary(self):
        """Print processing summary."""
        print("\n" + "="*60)
        print("PROCESSING SUMMARY")
        print("="*60)
        print(f"Successfully processed: {len(self.processed_files)} files")
        print(f"Skipped (no DWT marker): {len(self.skipped_files)} files")
        print(f"Errors: {len(self.error_files)} files")
        
        if self.error_files:
            print("\nFiles with errors:")
            for file in self.error_files:
                print(f"  - {file}")
        
        if self.skipped_files and self.verbose:
            print("\nSkipped files:")
            for file in self.skipped_files:
                print(f"  - {file}")


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="DWT Template Applier - CLI batch and single-file processing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --file page.html                   # Single file to stdout
  %(prog)s --file page.html --overwrite       # Overwrite single file
  %(prog)s --folder website/                  # Process folder recursively
  %(prog)s --folder pages/ --no-recursive     # Process folder only
  %(prog)s --folder website/ --output out/    # Output to different folder
  %(prog)s --folder website/ --dry-run        # Preview what would be processed
  %(prog)s --file page.html --debug           # Enable debug output
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--file', help='Process single HTML file')
    input_group.add_argument('--folder', help='Process folder containing HTML files')
    parser.add_argument('--no-recursive', action='store_true', 
                       help='Do not process subfolders (folder mode only)')
    
    # Output options
    parser.add_argument('--output', help='Output folder (folder mode) or file (file mode)')
    parser.add_argument('--overwrite', action='store_true',
                       help='Overwrite original files')
    
    # Processing options
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be processed without making changes')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug output from DWT processor')
    
    args = parser.parse_args()
    
    # Capture start time for update comments
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Enable debug mode if requested
    if args.debug:
        set_debug_mode(True)
    
    # Validate arguments
    if args.no_recursive and not args.folder:
        parser.error("--no-recursive can only be used with --folder")
    
    if args.file and args.overwrite and args.output:
        parser.error("Cannot use both --overwrite and --output with --file")
    
    processor = DWTUIProcessor(dry_run=args.dry_run, verbose=args.verbose, start_time=start_time)
    
    try:
        if args.file:
            # Single file processing
            if not os.path.isfile(args.file):
                print(f"Error: File '{args.file}' not found")
                sys.exit(1)
            
            output_file = args.output if args.output else None
            if args.overwrite and output_file:
                print("Warning: --output ignored when --overwrite is used")
                output_file = None
            processor.process_single_file(args.file, output_file, args.overwrite)
            
        elif args.folder:
            # Folder processing
            if not os.path.isdir(args.folder):
                print(f"Error: Folder '{args.folder}' not found")
                sys.exit(1)
            
            recursive = not args.no_recursive
            if args.overwrite and args.output:
                print("Warning: --output ignored when --overwrite is used")
                args.output = None
            processor.process_folder(args.folder, args.output, recursive, args.overwrite)
        
        processor.print_summary()
        
    except KeyboardInterrupt:
        print("\nProcessing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
