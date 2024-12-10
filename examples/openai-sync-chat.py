from scope3ai import Scope3AI
from openai import OpenAI


def interact() -> None:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello world"}],
        stream=False,
    )
    print(response.choices[0].message.content)
    print(response)
    return response


if __name__ == "__main__":
    scope3 = Scope3AI.init(enable_debug_logging=True)

    # 1. Using context
    # trace() will create a "tracer" that will record all the interactions
    # with a specific trace_id (UUID)
    # it can be used later to get the impact of the interactions
    with scope3.trace() as tracer:
        interact()
        print(tracer.impact())

    # # 2. Using context, but record trace_id for usage on global scope
    # # you could keep the trace_id and use it later
    # trace_id = None
    # with scope3.trace() as tracer:
    #     trace_id = tracer.trace_id
    #     interact()

    # print(scope3.impact(trace_id=trace_id))

    # # 3. Using record_id from the response
    # response = interact()
    # print(scope3.impact(record_id=response.scope3ai.record_id))

    # # 3.1 Alternative with many record_id
    # print(scope3.impact_many(record_ids=[response.scope3ai.record_id]))

    # # 4. Using sync mode to extend the response with the impact
    # # it always include impact in the response by querying the API on every call
    # scope3.include_impact_response = True
    # response = interact()
    # print(response.scope3ai.impact)
