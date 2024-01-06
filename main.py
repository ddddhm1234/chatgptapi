import chatgpt

gpt = chatgpt.ChatGPT()

print("\n=== 第一轮对话 ===")
print(gpt.ask("解释一下这段代码"))

print("\n=== 第二轮对话 ===")
print(gpt.ask("int main() {printf(\"Hello, word\";)}"))
