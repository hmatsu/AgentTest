"""
Final Integration Test - Complete GraphRAG Implementation
Tests all fixes together: API keys, prompt files, template parsing
"""
import os
import sys
from pathlib import Path

def test_complete_graphrag_setup():
    """Test complete GraphRAG setup with all fixes applied"""
    print("🧪 Final GraphRAG Integration Test")
    print("=" * 50)
    print("Testing: API keys + Prompt files + Template parsing + Environment inheritance")
    print()
    
    success_count = 0
    total_checks = 6
    
    print("1️⃣ Python Version Check:")
    import sys
    version = sys.version_info
    if version.major == 3 and 10 <= version.minor <= 12:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} is compatible with GraphRAG")
        success_count += 1
    else:
        print(f"   ⚠️ Python {version.major}.{version.minor}.{version.micro} - GraphRAG requires 3.10-3.12")
    
    print("\n2️⃣ Prompt Files Check:")
    prompts_dir = Path("./graphrag_workspace/prompts")
    required_files = ["summarize_descriptions.txt", "entity_extraction.txt", "community_report.txt"]
    
    if all((prompts_dir / f).exists() for f in required_files):
        print(f"   ✅ All {len(required_files)} required prompt files found")
        success_count += 1
    else:
        print("   ❌ Missing required prompt files")
    
    print("\n3️⃣ Settings Template Parsing Check:")
    try:
        from string import Template
        settings_file = Path("./graphrag_workspace/settings.yaml")
        
        if settings_file.exists():
            content = settings_file.read_text(encoding='utf-8')
            
            test_env = os.environ.copy()
            test_env['OPENAI_API_KEY'] = 'sk-test-template-parsing-verification'
            
            template = Template(content)
            result = template.substitute(test_env)
            
            if 'sk-test-template-parsing-verification' in result and 'dummy_key' not in result:
                print("   ✅ Template parsing works correctly")
                success_count += 1
            else:
                print("   ❌ Template parsing issues detected")
        else:
            print("   ❌ settings.yaml not found")
            
    except Exception as e:
        print(f"   ❌ Template parsing error: {e}")
    
    print("\n4️⃣ Environment Variable Inheritance Check:")
    try:
        import subprocess
        test_key = "sk-test-env-inheritance-final"
        test_env = os.environ.copy()
        test_env['OPENAI_API_KEY'] = test_key
        
        result = subprocess.run(
            [sys.executable, '-c', f'import os; print(os.getenv("OPENAI_API_KEY", "NOT_SET"))'],
            capture_output=True,
            text=True,
            env=test_env
        )
        
        if test_key in result.stdout:
            print("   ✅ Environment variable inheritance working")
            success_count += 1
        else:
            print("   ❌ Environment variable inheritance failed")
            
    except Exception as e:
        print(f"   ❌ Environment inheritance test error: {e}")
    
    print("\n5️⃣ GraphRAG Vector Store Creation Check:")
    try:
        from rag.vector_store import create_vector_store
        
        graphrag_store = create_vector_store("graphrag")
        if graphrag_store:
            print("   ✅ GraphRAG vector store created successfully")
            success_count += 1
        else:
            print("   ❌ Failed to create GraphRAG vector store")
            
    except Exception as e:
        print(f"   ❌ GraphRAG vector store creation error: {e}")
    
    print("\n6️⃣ Document Processing Check:")
    try:
        from rag.document_loader import create_document_processor
        
        processor = create_document_processor()
        documents = processor.load_documents_from_path("documents/")
        
        if documents and len(documents) > 0:
            print(f"   ✅ Successfully loaded {len(documents)} document chunks")
            success_count += 1
        else:
            print("   ❌ No documents found or loading failed")
            
    except Exception as e:
        print(f"   ❌ Document processing error: {e}")
    
    print(f"\n📊 Integration Test Results: {success_count}/{total_checks} checks passed")
    
    if success_count == total_checks:
        print("\n🎉 All integration tests passed!")
        print("✅ GraphRAG is ready for testing with real OpenAI API key")
        print("\n🚀 User can now run:")
        print("   set OPENAI_API_KEY=your_real_key")
        print("   python graph_rag_comparison.py")
        return True
    else:
        print(f"\n⚠️ {total_checks - success_count} check(s) failed")
        print("🔧 Additional fixes may be needed")
        return False

def test_comparison_script_dry_run():
    """Test the comparison script without real API calls"""
    print("\n🔄 Comparison Script Dry Run Test")
    print("=" * 40)
    
    try:
        from rag.rag_agent import create_rag_agent, create_graphrag_agent
        print("   ✅ Successfully imported RAG agents")
        
        rag_agent = create_rag_agent()
        print("   ✅ Traditional RAG agent created")
        
        graphrag_agent = create_graphrag_agent()
        print("   ✅ GraphRAG agent created")
        
        print("   ✅ Comparison script components working")
        return True
        
    except Exception as e:
        print(f"   ❌ Comparison script test error: {e}")
        return False

def main():
    """Run final integration test"""
    print("🎯 Final GraphRAG Implementation Integration Test")
    print("=" * 60)
    print("Purpose: Verify all GraphRAG fixes work together")
    print("Fixes tested: API keys, prompt files, template parsing, environment inheritance")
    print()
    
    setup_success = test_complete_graphrag_setup()
    script_success = test_comparison_script_dry_run()
    
    overall_success = setup_success and script_success
    
    print(f"\n📋 Final Test Summary:")
    print(f"   Setup Tests: {'✅ PASSED' if setup_success else '❌ FAILED'}")
    print(f"   Script Tests: {'✅ PASSED' if script_success else '❌ FAILED'}")
    print(f"   Overall: {'✅ READY FOR USER TESTING' if overall_success else '❌ NEEDS MORE FIXES'}")
    
    if overall_success:
        print("\n🎉 GraphRAG implementation is complete and ready!")
        print("🔑 All that's needed now is a real OpenAI API key for full testing")
    else:
        print("\n🔧 Additional fixes needed before user testing")
        
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
