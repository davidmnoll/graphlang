#include "../include/node_store.hpp"
#include <iostream>

void printNode(const NodeStore &store, const Hash &hash, const std::string &label)
{
  std::cout << label << " (hash: " << hash << "):\n";
  const Node &node = store.get(hash);
  for (const auto &edge : node.edges)
  {
    std::cout << "  Edge: (" << edge.first << ", " << edge.second << ")\n";
  }
  std::cout << "\n";
}

int main()
{
  try
  {
    NodeStore store;

    // Create basic nodes
    Hash empty = store.empty();
    Hash unit = store.unit();

    std::cout << "Created basic nodes:\n";
    printNode(store, empty, "Empty Node");
    printNode(store, unit, "Unit Node");

    // Create a pattern node: [(E,U), (U,E)]
    Node pattern;
    pattern.edges = {
        {empty, unit},
        {unit, empty}};
    Hash pattern_hash = store.store(pattern);
    printNode(store, pattern_hash, "Pattern Node");

    // Create an input node with similar structure
    Node input;
    input.edges = {
        {empty, unit},
        {unit, empty},
        {unit, unit} // Extra edge
    };
    Hash input_hash = store.store(input);
    printNode(store, input_hash, "Input Node");

    // Perform pattern matching
    Hash result = store.match(pattern_hash, input_hash);
    printNode(store, result, "Match Result");

    // Save the store to YAML
    store.saveToFile("graph_store.yaml");
    std::cout << "Saved store to graph_store.yaml\n";

    return 0;
  }
  catch (const std::exception &e)
  {
    std::cerr << "Error: " << e.what() << "\n";
    return 1;
  }
}