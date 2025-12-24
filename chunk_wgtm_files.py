#!/usr/bin/env python3
"""
WGTM (Web GTM) File Chunker
Parses large Web GTM Tag Assistant JSON files into smaller, manageable chunks.
Supports both Web GTM (wgtm) and Server GTM (sgtm) formats.
"""

import json
import csv
import argparse
from pathlib import Path
from typing import Dict, List, Any


class WGTMChunker:
    """Handles chunking of Web GTM Tag Assistant JSON files."""
    
    def __init__(self, output_dir: str = "chunked_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def chunk_json(self, input_file: str, chunk_by: str = "messages", max_items: int = 100) -> List[str]:
        """
        Parse a Web GTM Tag Assistant JSON file and split it into smaller chunks.
        
        Args:
            input_file: Path to the WGTM JSON file
            chunk_by: How to chunk ('messages', 'events', 'tags', 'datalayer', 'containers')
            max_items: Maximum items per chunk
        
        Returns:
            List of output file paths
        """
        print(f"📖 Reading WGTM file: {input_file}")
        print(f"   This may take a moment for large files...")
        
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        base_name = Path(input_file).stem
        context = data.get('data', {}).get('debugContext', 'UNKNOWN')
        print(f"   Detected context: {context} GTM")
        
        if chunk_by == "messages":
            output_files = self._chunk_messages(data, base_name, max_items)
        elif chunk_by == "events":
            output_files = self._chunk_events(data, base_name, max_items)
        elif chunk_by == "tags":
            output_files = self._chunk_tags(data, base_name, max_items)
        elif chunk_by == "datalayer":
            output_files = self._chunk_datalayer(data, base_name, max_items)
        elif chunk_by == "containers":
            output_files = self._chunk_containers(data, base_name, max_items)
        else:
            raise ValueError(f"Unknown chunk_by method: {chunk_by}")
        
        print(f"\n✅ Created {len(output_files)} chunk(s)")
        return output_files
    
    def _chunk_messages(self, data: Dict, base_name: str, max_per_chunk: int) -> List[str]:
        """Chunk by messages from all containers."""
        output_files = []
        all_messages = []
        
        for container in data.get('data', {}).get('containers', []):
            container_id = container.get('publicId', 'unknown')
            messages = container.get('messages', [])
            
            print(f"   Found {len(messages)} messages in container {container_id}")
            
            for msg in messages:
                all_messages.append({
                    '_container_id': container_id,
                    '_container_canonical_id': container.get('canonicalId'),
                    'message': msg
                })
        
        print(f"   Total messages: {len(all_messages)}")
        
        for i in range(0, len(all_messages), max_per_chunk):
            chunk_messages = all_messages[i:i + max_per_chunk]
            chunk_num = i // max_per_chunk + 1
            
            output_file = self.output_dir / f"{base_name}_messages_chunk_{chunk_num}.json"
            self._write_json({
                'chunk_number': chunk_num,
                'total_messages': len(chunk_messages),
                'messages': chunk_messages
            }, output_file)
            output_files.append(str(output_file))
        
        return output_files
    
    def _chunk_events(self, data: Dict, base_name: str, max_per_chunk: int) -> List[str]:
        """Chunk by unique event names."""
        output_files = []
        events_by_name = {}
        
        for container in data.get('data', {}).get('containers', []):
            container_id = container.get('publicId', 'unknown')
            messages = container.get('messages', [])
            
            for msg in messages:
                event_name = msg.get('eventNameKey', 'unknown_event')
                
                if event_name not in events_by_name:
                    events_by_name[event_name] = []
                
                events_by_name[event_name].append({
                    '_container_id': container_id,
                    'event_name': event_name,
                    'message': msg
                })
        
        print(f"   Found {len(events_by_name)} unique event types")
        
        for event_name, event_messages in events_by_name.items():
            safe_name = event_name.replace('.', '_').replace('/', '_').replace(':', '_')
            
            for i in range(0, len(event_messages), max_per_chunk):
                chunk_events = event_messages[i:i + max_per_chunk]
                chunk_num = i // max_per_chunk + 1
                
                if len(event_messages) > max_per_chunk:
                    output_file = self.output_dir / f"{base_name}_event_{safe_name}_chunk_{chunk_num}.json"
                else:
                    output_file = self.output_dir / f"{base_name}_event_{safe_name}.json"
                
                self._write_json({
                    'event_name': event_name,
                    'chunk_number': chunk_num,
                    'total_instances': len(chunk_events),
                    'events': chunk_events
                }, output_file)
                output_files.append(str(output_file))
        
        return output_files
    
    def _chunk_tags(self, data: Dict, base_name: str, max_per_chunk: int) -> List[str]:
        """Chunk by tags that were fired."""
        output_files = []
        all_tags = []
        
        for container in data.get('data', {}).get('containers', []):
            container_id = container.get('publicId', 'unknown')
            messages = container.get('messages', [])
            
            for msg in messages:
                tags_in_message = msg.get('tags', [])
                for tag in tags_in_message:
                    all_tags.append({
                        '_container_id': container_id,
                        '_event': msg.get('eventNameKey'),
                        '_message_index': msg.get('index'),
                        'tag': tag
                    })
        
        print(f"   Found {len(all_tags)} tag firings")
        
        for i in range(0, len(all_tags), max_per_chunk):
            chunk_tags = all_tags[i:i + max_per_chunk]
            chunk_num = i // max_per_chunk + 1
            
            output_file = self.output_dir / f"{base_name}_tags_chunk_{chunk_num}.json"
            self._write_json({
                'chunk_number': chunk_num,
                'total_tags': len(chunk_tags),
                'tags': chunk_tags
            }, output_file)
            output_files.append(str(output_file))
        
        return output_files
    
    def _chunk_datalayer(self, data: Dict, base_name: str, max_per_chunk: int) -> List[str]:
        """Chunk by dataLayer state in messages."""
        output_files = []
        all_datalayer_states = []
        
        for container in data.get('data', {}).get('containers', []):
            container_id = container.get('publicId', 'unknown')
            messages = container.get('messages', [])
            
            for msg in messages:
                if 'dataLayer' in msg:
                    all_datalayer_states.append({
                        '_container_id': container_id,
                        '_event': msg.get('eventNameKey'),
                        '_message_index': msg.get('index'),
                        'dataLayer': msg.get('dataLayer')
                    })
        
        print(f"   Found {len(all_datalayer_states)} dataLayer states")
        
        for i in range(0, len(all_datalayer_states), max_per_chunk):
            chunk_dl = all_datalayer_states[i:i + max_per_chunk]
            chunk_num = i // max_per_chunk + 1
            
            output_file = self.output_dir / f"{base_name}_datalayer_chunk_{chunk_num}.json"
            self._write_json({
                'chunk_number': chunk_num,
                'total_states': len(chunk_dl),
                'datalayer_states': chunk_dl
            }, output_file)
            output_files.append(str(output_file))
        
        return output_files
    
    def _chunk_containers(self, data: Dict, base_name: str, max_per_chunk: int) -> List[str]:
        """Chunk by GTM containers."""
        output_files = []
        containers = data.get('data', {}).get('containers', [])
        
        for i in range(0, len(containers), max_per_chunk):
            chunk_data = data.copy()
            chunk_data['data'] = data['data'].copy()
            chunk_data['data']['containers'] = containers[i:i + max_per_chunk]
            
            output_file = self.output_dir / f"{base_name}_containers_{i // max_per_chunk + 1}.json"
            self._write_json(chunk_data, output_file)
            output_files.append(str(output_file))
        
        return output_files
    
    def _write_json(self, data: Any, output_file: Path):
        """Write JSON data to file with pretty formatting."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        file_size = output_file.stat().st_size / (1024 * 1024)  # MB
        print(f"      ✓ {output_file.name} ({file_size:.2f} MB)")
    
    def generate_summary(self, input_file: str) -> Dict[str, Any]:
        """Generate a summary of the WGTM file contents."""
        print("📊 Analyzing file...")
        
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        containers = data.get('data', {}).get('containers', [])
        context = data.get('data', {}).get('debugContext', 'UNKNOWN')
        
        summary = {
            'file': Path(input_file).name,
            'type': f'{context} GTM Tag Assistant JSON',
            'file_size_mb': round(Path(input_file).stat().st_size / (1024 * 1024), 2),
            'name': data.get('name'),
            'version': data.get('version'),
            'debug_context': context,
            'container_count': len(containers),
            'containers': []
        }
        
        total_messages = 0
        event_types = {}
        
        for container in containers:
            messages = container.get('messages', [])
            total_messages += len(messages)
            
            # Count event types
            for msg in messages:
                event_name = msg.get('eventNameKey', 'unknown')
                event_types[event_name] = event_types.get(event_name, 0) + 1
            
            # Count tags
            total_tags = sum(len(msg.get('tags', [])) for msg in messages)
            
            container_info = {
                'id': container.get('publicId'),
                'canonical_id': container.get('canonicalId'),
                'product': container.get('product'),
                'message_count': len(messages),
                'total_tags_fired': total_tags,
                'has_errors': any(msg.get('hasError', False) for msg in messages)
            }
            summary['containers'].append(container_info)
        
        summary['total_messages'] = total_messages
        summary['unique_event_types'] = len(event_types)
        summary['event_types_top_20'] = dict(sorted(event_types.items(), key=lambda x: x[1], reverse=True)[:20])
        
        return summary


def main():
    parser = argparse.ArgumentParser(
        description='Chunk large Web GTM Tag Assistant JSON files into smaller files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get a summary first
  python chunk_wgtm_files.py tag_assistant_messerattach_com.json --summary-only
  
  # Chunk by messages (25 per chunk for ~2.5MB files)
  python chunk_wgtm_files.py tag_assistant_messerattach_com.json --max-items 25
  
  # Chunk by event type
  python chunk_wgtm_files.py tag_assistant_messerattach_com.json --chunk-by events --max-items 20
  
  # Chunk by tags fired
  python chunk_wgtm_files.py tag_assistant_messerattach_com.json --chunk-by tags
        """
    )
    
    parser.add_argument('input_file', help='Input WGTM JSON file to chunk')
    parser.add_argument('--output-dir', default='chunked_output',
                       help='Output directory for chunks (default: chunked_output)')
    parser.add_argument('--chunk-by', choices=['messages', 'events', 'tags', 'datalayer', 'containers'],
                       default='messages', help='How to chunk the file (default: messages)')
    parser.add_argument('--max-items', type=int, default=25,
                       help='Max items per chunk (default: 25)')
    parser.add_argument('--summary-only', action='store_true',
                       help='Only generate summary, do not chunk')
    
    args = parser.parse_args()
    
    chunker = WGTMChunker(output_dir=args.output_dir)
    
    if args.summary_only:
        summary = chunker.generate_summary(args.input_file)
        print("\n" + "="*80)
        print("FILE SUMMARY")
        print("="*80)
        print(json.dumps(summary, indent=2))
        return
    
    output_files = chunker.chunk_json(
        args.input_file,
        chunk_by=args.chunk_by,
        max_items=args.max_items
    )
    
    print(f"\n📁 Output files saved to: {args.output_dir}/")


if __name__ == '__main__':
    main()
