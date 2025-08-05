# scrape_appwrite_docs.py

from langchain_community.document_loaders import WebBaseLoader

# 🚀 WriteWise - Comprehensive Appwrite Documentation Links
# Use this list to feed your RAG system for maximum coverage!

APPWRITE_DOCS_URLS = [
    # 📚 Core Documentation
    "https://appwrite.io/docs",
    "https://appwrite.io/docs/overview",
    "https://appwrite.io/docs/getting-started",

    # 🔐 Authentication & Users
    "https://appwrite.io/docs/products/auth",
    "https://appwrite.io/docs/products/auth/quick-start",
    "https://appwrite.io/docs/products/auth/users",
    "https://appwrite.io/docs/products/auth/teams",
    "https://appwrite.io/docs/products/auth/sessions",
    "https://appwrite.io/docs/products/auth/oauth2",
    "https://appwrite.io/docs/products/auth/email-password",
    "https://appwrite.io/docs/products/auth/phone-sms",
    "https://appwrite.io/docs/products/auth/magic-url",
    "https://appwrite.io/docs/products/auth/anonymous",
    "https://appwrite.io/docs/products/auth/server-side-rendering",

    # 🗄️ Databases
    "https://appwrite.io/docs/products/databases",
    "https://appwrite.io/docs/products/databases/quick-start",
    "https://appwrite.io/docs/products/databases/collections",
    "https://appwrite.io/docs/products/databases/documents",
    "https://appwrite.io/docs/products/databases/queries",
    "https://appwrite.io/docs/products/databases/permissions",
    "https://appwrite.io/docs/products/databases/relationships",
    "https://appwrite.io/docs/products/databases/indexing",

    # ⚡ Functions
    "https://appwrite.io/docs/products/functions",
    "https://appwrite.io/docs/products/functions/quick-start",
    "https://appwrite.io/docs/products/functions/develop",
    "https://appwrite.io/docs/products/functions/deploy",
    "https://appwrite.io/docs/products/functions/execution",
    "https://appwrite.io/docs/products/functions/templates",
    "https://appwrite.io/docs/products/functions/runtimes",

    # 📁 Storage
    "https://appwrite.io/docs/products/storage",
    "https://appwrite.io/docs/products/storage/quick-start",
    "https://appwrite.io/docs/products/storage/buckets",
    "https://appwrite.io/docs/products/storage/upload-download",
    "https://appwrite.io/docs/products/storage/permissions",
    "https://appwrite.io/docs/products/storage/image-transformations",

    # 📧 Messaging
    "https://appwrite.io/docs/products/messaging",
    "https://appwrite.io/docs/products/messaging/quick-start",
    "https://appwrite.io/docs/products/messaging/email",
    "https://appwrite.io/docs/products/messaging/sms",
    "https://appwrite.io/docs/products/messaging/push-notifications",
    "https://appwrite.io/docs/products/messaging/topics",
    "https://appwrite.io/docs/products/messaging/subscribers",

    # 🌐 Sites
    "https://appwrite.io/docs/products/sites",
    "https://appwrite.io/docs/products/sites/quick-start",
    "https://appwrite.io/docs/products/sites/deploy",
    "https://appwrite.io/docs/products/sites/custom-domains",
    "https://appwrite.io/docs/products/sites/environment-variables",

    # 📊 Realtime
    "https://appwrite.io/docs/apis/realtime",
    "https://appwrite.io/docs/products/databases/realtime",

    # 🚀 Quick Starts by Platform
    "https://appwrite.io/docs/quick-starts/web",
    "https://appwrite.io/docs/quick-starts/react",
    "https://appwrite.io/docs/quick-starts/vue",
    "https://appwrite.io/docs/quick-starts/angular",
    "https://appwrite.io/docs/quick-starts/svelte",
    "https://appwrite.io/docs/quick-starts/nextjs",
    "https://appwrite.io/docs/quick-starts/nuxt",
    "https://appwrite.io/docs/quick-starts/sveltekit",
    "https://appwrite.io/docs/quick-starts/android",
    "https://appwrite.io/docs/quick-starts/apple",
    "https://appwrite.io/docs/quick-starts/flutter",
    "https://appwrite.io/docs/quick-starts/react-native",

    # 📱 SDK Documentation
    "https://appwrite.io/docs/sdks",
    "https://appwrite.io/docs/sdks/web",
    "https://appwrite.io/docs/sdks/flutter",
    "https://appwrite.io/docs/sdks/android",
    "https://appwrite.io/docs/sdks/apple",
    "https://appwrite.io/docs/sdks/react-native",
    "https://appwrite.io/docs/sdks/node",
    "https://appwrite.io/docs/sdks/python",
    "https://appwrite.io/docs/sdks/php",
    "https://appwrite.io/docs/sdks/dart",
    "https://appwrite.io/docs/sdks/ruby",
    "https://appwrite.io/docs/sdks/deno",
    "https://appwrite.io/docs/sdks/dotnet",
    "https://appwrite.io/docs/sdks/kotlin",
    "https://appwrite.io/docs/sdks/swift",

    # 🔌 API References
    "https://appwrite.io/docs/references",
    "https://appwrite.io/docs/references/cloud/client-web/account",
    "https://appwrite.io/docs/references/cloud/client-web/databases",
    "https://appwrite.io/docs/references/cloud/client-web/functions",
    "https://appwrite.io/docs/references/cloud/client-web/storage",
    "https://appwrite.io/docs/references/cloud/client-web/teams",
    "https://appwrite.io/docs/references/cloud/client-web/users",
    "https://appwrite.io/docs/references/cloud/client-web/messaging",
    "https://appwrite.io/docs/references/cloud/client-web/locale",
    "https://appwrite.io/docs/references/cloud/client-web/avatars",
    "https://appwrite.io/docs/references/cloud/server-nodejs/account",
    "https://appwrite.io/docs/references/cloud/server-nodejs/databases",
    "https://appwrite.io/docs/references/cloud/server-nodejs/functions",
    "https://appwrite.io/docs/references/cloud/server-nodejs/storage",
    "https://appwrite.io/docs/references/cloud/server-nodejs/users",
    "https://appwrite.io/docs/references/cloud/server-nodejs/teams",
    "https://appwrite.io/docs/references/cloud/server-nodejs/messaging",

    # 🛠️ Advanced Topics
    "https://appwrite.io/docs/advanced/platform",
    "https://appwrite.io/docs/advanced/migrations",
    "https://appwrite.io/docs/advanced/security",
    "https://appwrite.io/docs/advanced/self-hosting",
    "https://appwrite.io/docs/advanced/self-hosting/installation",
    "https://appwrite.io/docs/advanced/self-hosting/configuration",
    "https://appwrite.io/docs/advanced/self-hosting/docker",
    "https://appwrite.io/docs/advanced/self-hosting/environment-variables",
    "https://appwrite.io/docs/advanced/self-hosting/functions",
    "https://appwrite.io/docs/advanced/self-hosting/email-delivery",
    "https://appwrite.io/docs/advanced/self-hosting/ssl",
    "https://appwrite.io/docs/advanced/self-hosting/custom-domain",

    # 🎓 Tutorials & Guides
    "https://appwrite.io/docs/tutorials/react",
    "https://appwrite.io/docs/tutorials/vue",
    "https://appwrite.io/docs/tutorials/svelte",
    "https://appwrite.io/docs/tutorials/angular",
    "https://appwrite.io/docs/tutorials/flutter",
    "https://appwrite.io/docs/tutorials/android",
    "https://appwrite.io/docs/tutorials/nextjs",
    "https://appwrite.io/docs/tutorials/nuxt",
    "https://appwrite.io/docs/tutorials/sveltekit",

    # 🔧 Tools & Utilities
    "https://appwrite.io/docs/tooling/command-line",
    "https://appwrite.io/docs/tooling/migrations",
    "https://appwrite.io/docs/apis/graphql",
    "https://appwrite.io/docs/apis/rest",
    "https://appwrite.io/docs/apis/realtime",

    # 🌍 Additional Services
    "https://appwrite.io/docs/products/locale",
    "https://appwrite.io/docs/products/avatars",

    # 🔍 Specific Features
    "https://appwrite.io/docs/products/auth/password-history",
    "https://appwrite.io/docs/products/auth/password-dictionary",
    "https://appwrite.io/docs/products/databases/backup",
    "https://appwrite.io/docs/products/functions/logging",
    "https://appwrite.io/docs/products/storage/encryption",
    "https://appwrite.io/docs/products/messaging/templates",
]

# 🎯 Pro tip: Use these URLs to:
# 1. Scrape comprehensive Appwrite documentation
# 2. Create embeddings for your RAG system
# 3. Build a knowledge base that covers ALL Appwrite features
# 4. Make WriteWise the ultimate Appwrite expert!

print(f"🚀 Total Appwrite Documentation URLs: {len(APPWRITE_DOCS_URLS)}")
print("Ready to make WriteWise incredibly powerful! 💪")

def scrape_appwrite_docs():
    print("Scraping Appwrite documentation...")
    loader = WebBaseLoader(APPWRITE_DOCS_URLS)
    docs = loader.load()
    print(f"✅ Scraped {len(docs)} documents.")
    return docs

if __name__ == "__main__":
    documents = scrape_appwrite_docs()
    for i, doc in enumerate(documents[:3]):
        print(f"\n📄 Document {i+1} Preview:")
        print(doc.page_content[:300])  # Preview first 300 chars
