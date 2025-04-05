from rag.chains.graph_qa import GraphSparqlQAChain
from rag.schemas.promptmanager import PromptManager

# Initialize the prompt manager
prompt_manager = PromptManager('prompts/')


# region graph queries
def get_machines_names(graph):
    """
    Retrieves the names of the machines from the RDF graph.

    Args:
        graph: The RDF graph containing the machine data.

    Returns:
        A list of machine names.
    """
    # Query to retrieve the names of the machines
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX sa-ontology: <http://www.semanticweb.org/raffi/ontologies/2024/10/sa-ontology#>
    
    SELECT DISTINCT ?machine_name
    WHERE {
        ?machine sa-ontology:id ?machine_name .
        ?machine sa-ontology:producesKPI ?kpi .
    }
    """

    # Execute the query and retrieve the results
    results = graph.query(query)

    # Extract the machine names from the results
    machine_names = [str(result['machine_name']) for result in results]

    return machine_names


# endregion


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
        self._llm = llm
        self._graph = graph

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
            self._llm, graph=self._graph, verbose=True, allow_dangerous_requests=True,
            sparql_select_prompt=general_QA_prompt_select, qa_prompt=general_QA_prompt_answer
        )
