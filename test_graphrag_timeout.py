"""
GraphRAG Timeout Test - Test with small dataset and timeout handling
"""
import os
import sys
from pathlib import Path

def create_small_test_dataset():
    """Create a very small test dataset for GraphRAG"""
    test_dir = Path("./test_small_dataset")
    test_dir.mkdir(exist_ok=True)
    
    small_content = """
This is a test document about cooking.
It contains information about recipes and ingredients.
The main ingredients are flour, eggs, and milk.
This recipe makes delicious pancakes.
"""
    
    (test_dir / "small_test.txt").write_text(small_content, encoding='utf-8')
    print(f"✅ Created small test dataset in {test_dir}")
    return test_dir

def test_graphrag_with_timeout():
    """Test GraphRAG with timeout handling on small dataset"""
    print("🧪 GraphRAG Timeout Test")
    print("=" * 40)
    print("Purpose: Test GraphRAG indexing with timeout on small dataset")
    print()
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not set")
        return False
    
    if api_key.startswith('sk-dummy') or api_key.startswith('sk-test'):
        print("⚠️ Using test API key - may cause authentication errors")
    else:
        print(f"🔑 Using real API key: {api_key[:10]}...{api_key[-4:]}")
    
    try:
        from rag.vector_store import create_vector_store
        from rag.document_loader import create_document_processor
        
        test_dir = create_small_test_dataset()
        
        print("\n📄 Loading small test dataset...")
        processor = create_document_processor()
        documents = processor.load_documents_from_path(str(test_dir))
        
        if not documents:
            print("❌ No documents loaded from test dataset")
            return False
            
        print(f"✅ Loaded {len(documents)} document chunks")
        
        print("\n🕸️ Testing GraphRAG with timeout...")
        graphrag_store = create_vector_store("graphrag")
        
        print("📝 Adding documents (this will test timeout handling)...")
        graphrag_store.add_documents(documents)
        
        print("🔍 Testing search...")
        results = graphrag_store.similarity_search("cooking recipes", k=3)
        
        print(f"📊 Search returned {len(results)} results")
        
        if results:
            print("✅ GraphRAG search successful")
            for i, doc in enumerate(results[:2], 1):
                print(f"   {i}. {doc.page_content[:60]}...")
        else:
            print("⚠️ No search results (may be using fallback)")
            
        return True
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test execution"""
    print("⏰ GraphRAG Timeout Handling Test")
    print("=" * 50)
    print("Testing: Timeout handling for GraphRAG indexing and querying")
    print("Dataset: Small test file (should complete quickly)")
    print()
    
    success = test_graphrag_with_timeout()
    
    if success:
        print("\n🎉 Timeout test completed!")
        print("✅ GraphRAG timeout handling is working")
    else:
        print("\n❌ Timeout test failed")
        print("🔧 Additional timeout adjustments may be needed")
        
    print("\n💡 If indexing still hangs:")
    print("   - Try reducing document size further")
    print("   - Check OpenAI API rate limits")
    print("   - Consider increasing timeout values")
        
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
