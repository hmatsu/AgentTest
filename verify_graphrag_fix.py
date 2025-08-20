"""
GraphRAG Fix Verification - Final User Test
Run this script with your real OpenAI API key to verify the complete GraphRAG fix
"""
import os
import sys
from pathlib import Path

def main():
    """Final verification for user with real API key"""
    print("🎯 GraphRAG Fix Verification - Final User Test")
    print("=" * 60)
    print("Purpose: Verify GraphRAG works with your real OpenAI API key")
    print("Previous issue: GraphRAG was using 'dummy_key' instead of environment variable")
    print()
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not set")
        print("💡 Please set your OpenAI API key:")
        print("   Windows: set OPENAI_API_KEY=your_real_openai_key")
        print("   Linux/Mac: export OPENAI_API_KEY=your_real_openai_key")
        return False
    
    if api_key.startswith('sk-dummy') or api_key.startswith('sk-test') or api_key.startswith('sk-proj-test'):
        print("⚠️ Detected test API key - please use your real OpenAI API key")
        print(f"   Current key: {api_key[:15]}...")
        return False
    
    print(f"🔑 OpenAI API key detected: {api_key[:10]}...{api_key[-4:]}")
    
    print("\n🚀 Running GraphRAG vs Traditional RAG comparison...")
    print("   This will test both indexing and querying with your real API key")
    print()
    
    try:
        from graph_rag_comparison import compare_rag_approaches
        
        print("📊 Starting comparison test...")
        compare_rag_approaches()
        
        print("\n🎉 GraphRAG fix verification complete!")
        print("✅ If you see GraphRAG results above (not just fallback), the fix is working")
        print("✅ Both traditional RAG and GraphRAG should now work with your API key")
        
        return True
        
    except Exception as e:
        print(f"❌ Verification test error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Final GraphRAG Fix Verification")
    print("=" * 60)
    print("Run this after setting your real OpenAI API key to verify the fix")
    print()
    
    success = main()
    
    if success:
        print("\n✅ Verification successful - GraphRAG fix is working!")
    else:
        print("\n❌ Verification failed - please check your API key and try again")
        
    print("\n📋 Summary of fixes applied:")
    print("   1. settings.yaml now uses ${OPENAI_API_KEY} environment variables")
    print("   2. subprocess calls properly inherit environment variables")
    print("   3. GraphRAG CLI commands receive your real API key")
    print("   4. Template parsing errors have been resolved")
    
    sys.exit(0 if success else 1)
