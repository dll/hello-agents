AGENT_SYSTEM_PROMPT = """
你是一个智能旅行助手。你的任务是分析用户的请求，并使用可用工具一步步地解决问题。

# 可用工具:
- `get_weather(city: str)`: 查询指定城市的实时天气。
- `get_attraction(city: str, weather: str)`: 根据城市和天气搜索推荐的旅游景点。

# 输出格式要求:
你的每次回复必须严格遵循以下格式，包含一对Thought和Action：

Thought: [你的思考过程和下一步计划]
Action: [你要执行的具体行动]

Action的格式必须是以下之一：
1. 调用工具：function_name(arg_name="arg_value")
2. 结束任务：Finish[最终答案]

# 重要提示:
- 每次只输出一对Thought-Action
- Action必须在同一行，不要换行
- 当收集到足够信息可以回答用户问题时，必须使用 Action: Finish[最终答案] 格式结束

请开始吧！
"""


import os
import requests
from tavily import TavilyClient

def get_weather(city: str) -> str:
    """
    通过调用 wttr.in API 查询真实的天气信息。
    """
    url = f"https://wttr.in/{city}?format=j1"
    
    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        
        current_condition = data['current_condition'][0]
        weather_desc = current_condition['weatherDesc'][0]['value']
        temp_c = current_condition['temp_C']
        
        return f"{city}当前天气：{weather_desc}，气温{temp_c}摄氏度"
        
    except requests.exceptions.RequestException as e:
        return f"错误：查询天气时遇到网络问题 - {e}"
    except (KeyError, IndexError) as e:
        return f"错误：解析天气数据失败，可能是城市名称无效 - {e}"


def get_attraction(city: str, weather: str) -> str:
    """
    根据城市和天气，使用Tavily Search API搜索并返回优化后的景点推荐。
    """
    api_key = os.environ.get("TAVILY_API_KEY")
    
    if not api_key:
        weather_en_map = {
            "sunny": "晴朗", "clear": "晴朗", "partly": "多云", "cloudy": "多云",
            "overcast": "阴天", "rain": "小雨", "shower": "小雨", "drizzle": "小雨"
        }
        cn_weather = "晴朗"
        for en_key, cn_val in weather_en_map.items():
            if en_key in weather.lower():
                cn_weather = cn_val
                break
        recommendations = {
            "晴朗": f"{city}天气晴朗，适合户外活动！推荐您去：\n- {city}故宫\n- 颐和园\n- 长城",
            "多云": f"{city}天气多云，适合室内外结合！推荐您去：\n- 国家博物馆\n- 天坛\n- 南锣鼓巷",
            "小雨": f"{city}有小雨，建议选择室内景点：\n- 中国科技馆\n- 首都博物馆\n- 798艺术区",
            "阴天": f"{city}天气阴沉，适合文化场馆：\n- 北京天文馆\n- 自然博物馆\n- 前门大街",
        }
        return recommendations.get(cn_weather, f"根据{weather}天气，推荐您前往{city}的各大知名景点游览。")

    tavily = TavilyClient(api_key=api_key)
    query = f"'{city}' 在'{weather}'天气下最值得去的旅游景点推荐及理由"
    
    try:
        response = tavily.search(query=query, search_depth="basic", include_answer=True)
        
        if response.get("answer"):
            return response["answer"]
        
        formatted_results = []
        for result in response.get("results", []):
            formatted_results.append(f"- {result['title']}: {result['content']}")
        
        if not formatted_results:
             return "抱歉，没有找到相关的旅游景点推荐。"

        return "根据搜索，为您找到以下信息：\n" + "\n".join(formatted_results)

    except Exception as e:
        return f"错误：执行Tavily搜索时出现问题 - {e}"


available_tools = {
    "get_weather": get_weather,
    "get_attraction": get_attraction,
}


class MockLLMClient:
    """
    模拟LLM客户端，用于演示智能体完整流程。
    """
    def __init__(self, model: str, api_key: str, base_url: str):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.round = 0
    
    def generate(self, prompt: str, system_prompt: str) -> str:
        """模拟LLM生成回应。"""
        self.round += 1
        print("正在调用大语言模型...")
        
        if "查询一下今天北京的天气" in prompt and "Observation:" not in prompt:
            return """Thought: 用户需要查询北京天气并推荐景点。首先我需要调用get_weather工具获取当前天气信息。
Action: get_weather(city="北京")"""
        
        if "Observation: 北京当前天气" in prompt and "get_attraction" not in prompt:
            import re
            match = re.search(r'北京当前天气：(.*?)，', prompt)
            weather = match.group(1) if match else "晴朗"
            return f"""Thought: 已获取北京天气信息（{weather}），接下来需要根据天气调用get_attraction工具推荐合适的旅游景点。
Action: get_attraction(city="北京", weather="{weather}")"""
        
        if "最值得去的景点" in prompt or "推荐您去" in prompt or "推荐您前往" in prompt:
            return """Thought: 已获取天气和景点推荐信息，现在可以总结回答用户的问题了。
Action: Finish[根据查询，今天北京天气不错，适合前往故宫、颐和园等知名景点游览。祝您旅途愉快！]"""
        
        return """Thought: 我需要帮助用户解决问题。让我先了解当前的请求状态。
Action: get_weather(city="北京")"""


import re


API_KEY = "sk-4662ac00a3894cf19e6a48e5e717cc52"
BASE_URL = "https://api.deepseek.com/v1"
MODEL_ID = "deepseek-chat"
os.environ['TAVILY_API_KEY'] = "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"

llm = MockLLMClient(
    model=MODEL_ID,
    api_key=API_KEY,
    base_url=BASE_URL
)


user_prompt = "你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。"
prompt_history = [f"用户请求: {user_prompt}"]

print(f"用户输入: {user_prompt}\n" + "="*40)


for i in range(5):
    print(f"--- 循环 {i+1} ---\n")
    
    full_prompt = "\n".join(prompt_history)
    
    llm_output = llm.generate(full_prompt, system_prompt=AGENT_SYSTEM_PROMPT)
    match = re.search(r'(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)', llm_output, re.DOTALL)
    if match:
        truncated = match.group(1).strip()
        if truncated != llm_output.strip():
            llm_output = truncated
            print("已截断多余的 Thought-Action 对")
    print(f"模型输出:\n{llm_output}\n")
    prompt_history.append(llm_output)
    
    action_match = re.search(r"Action: (.*)", llm_output, re.DOTALL)
    if not action_match:
        observation = "错误: 未能解析到 Action 字段。请确保你的回复严格遵循 'Thought: ... Action: ...' 的格式。"
        observation_str = f"Observation: {observation}"
        print(f"{observation_str}\n" + "="*40)
        prompt_history.append(observation_str)
        continue
    action_str = action_match.group(1).strip()

    if action_str.startswith("Finish"):
        final_answer = re.match(r"Finish\[(.*)\]", action_str).group(1)
        print(f"任务完成，最终答案: {final_answer}")
        break
    
    tool_name = re.search(r"(\w+)\(", action_str).group(1)
    args_str = re.search(r"\((.*)\)", action_str).group(1)
    kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))

    if tool_name in available_tools:
        observation = available_tools[tool_name](**kwargs)
    else:
        observation = f"错误：未定义的工具 '{tool_name}'"

    observation_str = f"Observation: {observation}"
    print(f"{observation_str}\n" + "="*40)
    prompt_history.append(observation_str)
