from services.llm_service import ask_llm

response = ask_llm(
    "Réponds uniquement par OK"
)

print(response)