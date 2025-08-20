"""
Test User's Exact Scenario - GraphRAG with Real API Key
Simulates the user's exact workflow with recipes_short.csv and real API key
"""
import os
import sys
from pathlib import Path

def test_user_scenario():
    """Test the exact scenario the user is experiencing"""
    print("🧪 Testing User's Exact GraphRAG Scenario")
    print("=" * 50)
    print("Scenario: recipes_short.csv (828 chunks) + real OpenAI API key")
    print()
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ No OPENAI_API_KEY environment variable set")
        print("💡 User should run: set OPENAI_API_KEY=your_real_key")
        return False
    
    print(f"🔑 API Key detected: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else '***'}")
    
    print("\n1️⃣ Testing settings.yaml API key substitution:")
    try:
        from string import Template
        
        settings_file = Path('./graphrag_workspace/settings.yaml')
        if settings_file.exists():
            content = settings_file.read_text(encoding='utf-8')
            template = Template(content)
            result = template.substitute(os.environ)
            
            if 'dummy_key' in result:
                print("   ❌ settings.yaml still contains dummy_key after substitution")
                return False
            else:
                print("   ✅ settings.yaml properly substitutes API key from environment")
                
        else:
            print("   ❌ settings.yaml not found")
            return False
            
    except Exception as e:
        print(f"   ❌ Settings substitution error: {e}")
        return False
    
    print("\n2️⃣ Testing GraphRAG with recipes_short.csv:")
    try:
        from rag.vector_store import create_vector_store
        from rag.document_loader import create_document_processor
        
        processor = create_document_processor()
        documents = processor.load_documents_from_path("documents/")
        
        if not documents:
            print("   ❌ No documents found in documents/ directory")
            return False
            
        print(f"   📄 Loaded {len(documents)} document chunks")
        
        graphrag_store = create_vector_store("graphrag")
        print("   🕸️ Created GraphRAG vector store")
        
        graphrag_store.add_documents(documents)
        print("   ✅ Added documents to GraphRAG store")
        
        results = graphrag_store.similarity_search("recipe ingredients cooking", k=3)
        print(f"   🔍 Search returned {len(results)} results")
        
        if results:
            print("   📋 Sample results:")
            for i, doc in enumerate(results[:2], 1):
                print(f"      {i}. {doc.page_content[:80]}...")
            return True
        else:
            print("   ⚠️ No search results (may indicate indexing issue)")
            return False
            
    except Exception as e:
        print(f"   ❌ GraphRAG test error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n3️⃣ Testing full RAG vs GraphRAG comparison:")
    try:
        from rag.rag_agent import create_rag_agent, create_graphrag_agent
        
        print("   📊 Creating traditional RAG agent...")
        rag_agent = create_rag_agent()
        rag_agent.add_documents_from_path("documents/")
        
        print("   🕸️ Creating GraphRAG agent...")
        graphrag_agent = create_graphrag_agent()
        graphrag_agent.add_documents_from_path("documents/")
        
        query = "What ingredients are commonly used in recipes?"
        
        print(f"   🔍 Testing query: {query}")
        
        print("   📊 Traditional RAG response:")
        rag_result = rag_agent.chat(query)
        print(f"      {rag_result[:100]}...")
        
        print("   🕸️ GraphRAG response:")
        graphrag_result = graphrag_agent.chat(query)
        print(f"      {graphrag_result[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Full comparison test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test execution"""
    print("🎯 User Scenario Test - GraphRAG with Real API Key")
    print("=" * 60)
    print("Purpose: Reproduce and fix user's 'dummy_key' authentication error")
    print()
    
    success = test_user_scenario()
    
    if success:
        print("\n🎉 User scenario test successful!")
        print("✅ GraphRAG should now work with user's real API key")
        print("✅ Ready for user to test: python graph_rag_comparison.py")
    else:
        print("\n❌ User scenario test failed")
        print("🔧 Additional fixes needed for GraphRAG API key configuration")
        
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
