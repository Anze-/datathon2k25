from rag.chains.graph_qa import GraphSparqlQAChain
from rag.schemas.promptmanager import PromptManager

# Initialize the prompt manager
prompt_manager = PromptManager('prompts/')


# GENERAL QA CHAIN
class GeneralQAChain:
    def __init__(self, llm, graph, history):
        """
        Initializes the GeneralQAChain to handle QA tasks related to graph-based queries.

        Args:
            llm: The language model to generate responses.
            graph: The RDF graph containing the data.
            history: A list of previous conversation entries to inform the context.
        """
        self.llm = llm
        self.graph = graph

        # Format the conversation history into a context string
        history_context = "CONVERSATION HISTORY:\n" + "\n\n".join(
            [f"Q: {entry['question']}\nA: {entry['answer']}" for entry in history]
        )

        self._history_context = history_context

        # Get the prompts for the QA tasks
        general_QA_prompt_select = prompt_manager.get_partial_init_prompt('qa_select', history_context=history_context)
        general_QA_prompt_answer = prompt_manager.get_prompt('qa_answer')

        # Initialize the chain that connects the prompts with the graph-based QA
        self.chain = GraphSparqlQAChain.from_llm(
            self.llm,
            graph=self.graph,
            verbose=True,
            allow_dangerous_requests=True,
            # sparql_select_prompt=general_QA_prompt_select,
            qa_prompt=general_QA_prompt_answer
        )

    @property
    def graph(self):
        return self._graph

    @graph.setter
    def graph(self, graph):
        self._graph = graph

    @property
    def llm(self):
        return self._llm

    @llm.setter
    def llm(self, llm):
        self._llm = llm
