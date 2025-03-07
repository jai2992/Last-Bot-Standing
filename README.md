# 🔐 Secret Key Discovery Chatbot  

Welcome to the **Secret Key Discovery Chatbot**! This chatbot guides users through a series of hints and puzzles, helping them find a secret key. It uses a **tree-based structure** and **LLM-powered dynamic hinting** to provide an adaptive user experience.

## 🚀 Features
- 🧩 **Riddle, math, and logic-based questions**  
- 🤖 **LLM-powered dynamic hint generation** for personalized assistance  
- 🔁 **Tracks user progress** in discovering the secret key  
- 🔄 **Asks multiple questions before revealing the next hint**  
- 🎯 **Adapts difficulty dynamically** based on user responses  
- 🏆 Successfully answering all hints leads to unlocking the **secret key!**  

---

## 🛠️ How It Works
1. The chatbot presents the **first question**.
2. The user submits an **answer**.
3. The chatbot **evaluates** the answer:
   - ✅ **Correct:** Proceeds to the next hint.
   - ❌ **Incorrect:**  
     - 📌 Provides a **dynamic hint** using an LLM model.  
     - 📊 Adapts hints based on user response patterns.  
     - 🔁 Continues until the correct answer is provided or a skip is chosen.  
4. The process continues until the user discovers the **secret key**. 🔑  

---

## 🔍 LLM-Powered Dynamic Hinting
- The chatbot **analyzes incorrect responses** and generates **contextual hints** using OpenAI's GPT model.  
- If users struggle, the chatbot **simplifies the question or rephrases it** for better understanding.  
- Instead of static hints, the chatbot **adapts difficulty dynamically** based on user progress.  

---

## 📜 Flowchart  
Below is a flowchart illustrating the chatbot’s **dynamic hinting system**:  

![Chatbot Flowchart](./chatbot_flowchart.png)

---


