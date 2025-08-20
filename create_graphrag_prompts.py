"""
Create missing GraphRAG prompt files
Extracts default prompt templates from the GraphRAG package
"""
import os
import sys
from pathlib import Path

def create_graphrag_prompts():
    """Create missing GraphRAG prompt files"""
    print("🔧 Creating missing GraphRAG prompt files...")
    
    prompts_dir = Path("./graphrag_workspace/prompts")
    prompts_dir.mkdir(exist_ok=True)
    
    try:
        from graphrag.prompt_tune.generator.entity_summarization_prompt import ENTITY_SUMMARIZATION_PROMPT
        from graphrag.prompt_tune.generator.entity_extraction_prompt import ENTITY_EXTRACTION_PROMPT
        from graphrag.prompt_tune.generator.community_report_prompt import COMMUNITY_REPORT_PROMPT
        
        summarize_file = prompts_dir / "summarize_descriptions.txt"
        with open(summarize_file, 'w', encoding='utf-8') as f:
            f.write(ENTITY_SUMMARIZATION_PROMPT)
        print(f"✅ Created {summarize_file}")
        
        entity_file = prompts_dir / "entity_extraction.txt"
        with open(entity_file, 'w', encoding='utf-8') as f:
            f.write(ENTITY_EXTRACTION_PROMPT)
        print(f"✅ Created {entity_file}")
        
        community_file = prompts_dir / "community_report.txt"
        with open(community_file, 'w', encoding='utf-8') as f:
            f.write(COMMUNITY_REPORT_PROMPT)
        print(f"✅ Created {community_file}")
        
        print(f"\n📁 Created {len(list(prompts_dir.glob('*.txt')))} prompt files in {prompts_dir}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import GraphRAG prompts: {e}")
        return False
    except Exception as e:
        print(f"❌ Error creating prompt files: {e}")
        return False

def create_fallback_prompts():
    """Create basic fallback prompt files if imports fail"""
    print("🔄 Creating fallback prompt files...")
    
    prompts_dir = Path("./graphrag_workspace/prompts")
    prompts_dir.mkdir(exist_ok=True)
    
    summarize_prompt = """
You are an AI assistant that helps summarize entity descriptions.

Given a list of entity descriptions, provide a comprehensive summary that captures the key information about each entity.

Entity Descriptions:
{entity_descriptions}

Summary:
"""
    
    entity_prompt = """
You are an AI assistant that extracts entities and relationships from text.

Extract all entities (people, organizations, locations, concepts) and their relationships from the following text:

Text:
{input_text}

Entities and Relationships:
"""
    
    community_prompt = """
You are an AI assistant that creates community reports.

Create a comprehensive report about the community based on the provided information:

Community Information:
{community_info}

Report:
"""
    
    try:
        files_created = []
        
        (prompts_dir / "summarize_descriptions.txt").write_text(summarize_prompt, encoding='utf-8')
        files_created.append("summarize_descriptions.txt")
        
        (prompts_dir / "entity_extraction.txt").write_text(entity_prompt, encoding='utf-8')
        files_created.append("entity_extraction.txt")
        
        (prompts_dir / "community_report.txt").write_text(community_prompt, encoding='utf-8')
        files_created.append("community_report.txt")
        
        for file in files_created:
            print(f"✅ Created fallback {file}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error creating fallback prompts: {e}")
        return False

def main():
    """Main execution"""
    print("🚀 GraphRAG Prompt Files Setup")
    print("=" * 40)
    print("Purpose: Fix FileNotFoundError for missing prompt files")
    print()
    
    if create_graphrag_prompts():
        print("\n🎉 Successfully created GraphRAG prompt files from package templates")
        return True
    else:
        print("\n⚠️ Failed to import GraphRAG prompts, trying fallback...")
        if create_fallback_prompts():
            print("\n🎉 Successfully created fallback prompt files")
            return True
        else:
            print("\n❌ Failed to create any prompt files")
            return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
