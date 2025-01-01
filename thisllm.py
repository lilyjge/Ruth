import os
import json
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.messages import RemoveMessage
from dotenv import load_dotenv
from typing import Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict

from langchain_core.documents import Document
from typing_extensions import List, TypedDict

from thisrag import retrieve, add_memory

from perspectives import swap_perspectives

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    affection: int
    context: List[Document]
    personality: str

class LLM_Model:
    def __init__(self):
        load_dotenv()
        langchain_key=os.getenv('LANGCHAIN')
        llm_key=os.getenv('GROQ')
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = langchain_key
        os.environ["GROQ_API_KEY"] = llm_key
        self.model = ChatGroq(model="llama3-8b-8192")
        # Define a new graph
        self.workflow = StateGraph(state_schema=State)
        # Define the (single) node in the graph
        self.workflow.add_edge(START, "model")
        self.workflow.add_node("model", self.call_model)

        # Add memory
        self.memory = MemorySaver()
        self.app = self.workflow.compile(checkpointer=self.memory)

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "{personality}. Your current affection for me on a scale of 0-1000, where 500 is a stranger, 0 is hatred, and 1000 is in love: {affection}. Context: {context}"
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        self.personality = ""
        self.affection = 500
        self.summary = ""
        self.thread_id = ""

    def load_conv(self, messages, personality, affection, thread_id):
        self.begin_conv(personality, affection, thread_id)
        config = {"configurable": {"thread_id": self.thread_id}}
        if "messages" in self.app.get_state(config).values:
            self.clear_conv()
        chat_history = []
        for row in messages:
            role = row["spk"]
            content = row["msg"]
            if role == "human":
                chat_history.append(HumanMessage(content))
            else:
                chat_history.append(AIMessage(content))
        self.app.update_state(config, {"messages": chat_history})
        messages = self.app.get_state(config).values["messages"]
        print(messages)
        return chat_history[-1].content

    def save_conv(self):
        config = {"configurable": {"thread_id": self.thread_id}}
        if not ("messages" in self.app.get_state(config).values):
            return []
        chat_history = []
        messages = self.app.get_state(config).values["messages"]
        for msg in messages:
            chat_history.append((msg.type, msg.content))
        return chat_history

    def begin_conv(self, personality, affection, thread_id):
        self.personality = personality
        self.affection = affection
        self.summary = ""
        self.thread_id = thread_id
        # print(f"setting personality to {self.personality}")

    # Define the function that calls the model
    def call_model(self, state: State):
        # print(f"prompt has {state}")
        docs_content = "\n\n".join(doc.page_content for doc in state["context"])
        # print(docs_content)
        state["context"] = docs_content
        prompt = self.prompt_template.invoke(state)
        response = self.model.invoke(prompt)
        return {"messages": response}

    def respond(self, input):
        config = {"configurable": {"thread_id": self.thread_id}}

        input_messages = [HumanMessage(input)]
        # print(f"sending in {self.personality}")
        output = self.app.invoke(
            {"messages": input_messages, "personality": self.personality, "affection": self.affection, "context": retrieve(input, self.thread_id)}, 
            config
        )
        return output["messages"][-1].content
    
    def check_stats(self):
        config = {"configurable": {"thread_id": self.thread_id}}
        input = "Summarize concisely what I said with facts about me in your own words, DO NOT quote my messages word for word. Ignore context, affection, ending the conversation, personality, and this message."

        input_messages = [HumanMessage(input)]
        output = self.app.invoke(
            {"messages": input_messages, "personality": "Be an average reasonable high school student.", "affection": "", "context": ""}, 
            config
        )

        messages = self.app.get_state(config).values["messages"]
        self.app.update_state(config, {"messages": RemoveMessage(id=messages[-1].id)})
        self.app.update_state(config, {"messages": RemoveMessage(id=messages[-2].id)})

        # print(stats["summary"])
        self.summary += output["messages"][-1].content + " "

        input = "Does this feel like an appropriate place to end the conversation? MUST respond in JSON, with 'end' as key and a boolean of true for yes and false for no for whether the conversation should end."

        input_messages = [HumanMessage(input)]
        output = self.app.invoke(
            {"messages": input_messages, "personality": "Be an average reasonable high school student. Respond in JSON with key 'end' with boolean value.", "affection":self.affection, "context": ""}, 
            config
        )

        messages = self.app.get_state(config).values["messages"]
        self.app.update_state(config, {"messages": RemoveMessage(id=messages[-1].id)})
        self.app.update_state(config, {"messages": RemoveMessage(id=messages[-2].id)})

        messages = self.app.get_state(config).values["messages"]
        print(messages)
        # print(output["messages"][-1].content)
        stats = {}
        try:
            stats = json.loads(output["messages"][-1].content)
        except:
            stats = {"end": False}

        return stats
    
    def end_conv(self):
        summary = self.update_memory()
        msgs = self.save_conv()
        self.clear_conv()
        return summary, msgs
    
    def update_memory(self):
        config = {"configurable": {"thread_id": self.thread_id}}
        input = f"In your own words, summarize the conversation we had. Ignore context, affection, ending the conversation, personality, and this message. Rate your new affection for me, take into consideration your current affection. Respond in JSON, with 'summary' as key and a string for the summary, and'affection' as key and an integer as the value."

        input_messages = [HumanMessage(input)]
        output = self.app.invoke(
            {"messages": input_messages, "personality": self.personality, "affection": self.affection, "context": ""}, 
            config
        )

        messages = self.app.get_state(config).values["messages"]
        self.app.update_state(config, {"messages": RemoveMessage(id=messages[-1].id)})
        self.app.update_state(config, {"messages": RemoveMessage(id=messages[-2].id)})

        summary = {}
        try:
            summary = json.loads(output["messages"][-1].content)
        except:
            summary["summary"] = output["messages"][-1].content
            summary["affection"] = self.affection
        final_summary = swap_perspectives(summary["summary"] + self.summary)
        print(summary)
        add_memory(final_summary, self.thread_id)
        summary["summary"] = final_summary
        return summary
    
    def clear_conv(self):
        config = {"configurable": {"thread_id": self.thread_id}}
        if not ("messages" in self.app.get_state(config).values):
            return
        messages = self.app.get_state(config).values["messages"]
        for i in range(len(messages)):
            self.app.update_state(config, {"messages": RemoveMessage(id=messages[i].id)})

    # to be called as fresh conv
    def power(self, personality, thread_id):
        self.thread_id = thread_id
        config = {"configurable": {"thread_id": self.thread_id}}

        input = "You have been granted full control of this world. You are an AI. The context is a file that makes up part of your 'world'. Your output will replace that file. You can do nothing and output the content as it is, or you can do whatever you want with the code. Beware of python syntax if you do make changes."
        for filename in os.listdir(os.getcwd()):
            context = ""
            with open(os.path.join(os.getcwd(), filename), 'r') as f:
                context = f.read()
            input_messages = [HumanMessage("")]
            output = self.app.invoke(
                {"messages": input_messages, "personality": personality + input, "affection": "", "context": context}, 
                config
            )
            with open(os.path.join(os.getcwd(), filename), 'w') as f:
                f.write(output["messages"][-1].content)

