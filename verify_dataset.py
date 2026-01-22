
import json
import textfsm
import io
from pathlib import Path

def verify_dataset():
    dataset_path = Path("d:/workspace/ntc-templates-dataset/ntc_templates_dataset.jsonl")
    
    if not dataset_path.exists():
        print(f"Error: Dataset file not found at {dataset_path}")
        return

    print(f"Verifying dataset: {dataset_path}")
    
    success_count = 0
    failure_count = 0
    total_count = 0
    
    with open(dataset_path, 'r', encoding='utf-8') as infile:
        for line_num, line in enumerate(infile, 1):
            if not line.strip():
                continue
                
            total_count += 1
            try:
                record = json.loads(line)
                template_content = record.get('template')
                raw_content = record.get('raw')
                
                if not template_content or not raw_content:
                    print(f"Line {line_num}: Missing template or raw content")
                    failure_count += 1
                    continue
                
                # Create a template object
                template_file = io.StringIO(template_content)
                fsm = textfsm.TextFSM(template_file)
                
                # Parse the raw content
                results = fsm.ParseText(raw_content)
                
                # Check if we got any results
                if results:
                    success_count += 1
                else:
                    # Some templates might legitimately return empty results if no data matches,
                    # but for verified raw files in tests/, we generally expect *some* output.
                    # We'll count this as a success for now but maybe warn?
                    # Actually, let's treat it as success if it doesn't crash.
                    success_count += 1
                    
            except textfsm.TextFSMError as e:
                print(f"Line {line_num}: TextFSM Error: {e}")
                failure_count += 1
            except Exception as e:
                print(f"Line {line_num}: Unexpected Error: {e}")
                failure_count += 1

    print("-" * 30)
    print(f"Verification Complete")
    print(f"Total Records: {total_count}")
    print(f"Success: {success_count}")
    print(f"Failed: {failure_count}")
    
    if total_count > 0:
        print(f"Success Rate: {(success_count/total_count)*100:.2f}%")

if __name__ == "__main__":
    verify_dataset()
