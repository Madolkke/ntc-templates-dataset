
import os
import json
from pathlib import Path

def create_dataset():
    # Define paths
    base_dir = Path(r"d:/workspace/ntc-templates-dataset/ntc-templates")
    templates_dir = base_dir / "ntc_templates" / "templates"
    tests_dir = base_dir / "tests"
    output_file = Path(r"d:/workspace/ntc-templates-dataset/ntc_templates_dataset.jsonl")

    print(f"Scanning for templates and raw files in {base_dir}...")
    
    records_count = 0
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Iterate over platform directories in tests/
        for platform_path in tests_dir.iterdir():
            if not platform_path.is_dir() or platform_path.name.startswith(('.', '__')) or platform_path.name == 'mocks':
                continue
            
            platform_name = platform_path.name
            
            # Iterate over command directories within the platform
            for command_path in platform_path.iterdir():
                if not command_path.is_dir():
                    continue
                
                command_name = command_path.name
                
                # Construct expected template filename
                # Convention: {platform}_{command}.textfsm
                template_filename = f"{platform_name}_{command_name}.textfsm"
                template_path = templates_dir / template_filename
                
                if not template_path.exists():
                    # Try explicit mapping if simple convention fails? 
                    # For now, skip if not found as per strict NTC convention
                    # print(f"Warning: Template not found for {platform_name} {command_name} at {template_path}")
                    continue
                
                try:
                    template_content = template_path.read_text(encoding='utf-8')
                except Exception as e:
                    print(f"Error reading template {template_path}: {e}")
                    continue

                # Find all .raw files in the command directory
                raw_files = list(command_path.glob("*.raw"))
                
                for raw_file in raw_files:
                    try:
                        raw_content = raw_file.read_text(encoding='utf-8')
                        
                        record = {
                            "template": template_content,
                            "raw": raw_content
                        }
                        
                        outfile.write(json.dumps(record, ensure_ascii=False) + '\n')
                        records_count += 1
                        
                    except Exception as e:
                        print(f"Error reading raw file {raw_file}: {e}")

    print(f"Dataset generation complete.")
    print(f"Total records created: {records_count}")
    print(f"Output saved to: {output_file}")

if __name__ == "__main__":
    create_dataset()
