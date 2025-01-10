#include "node_store.hpp"
#include <sstream>
#include <fstream>
#include <iomanip>
#include <openssl/sha.h>
#include <algorithm>
#include <stdexcept>

// Helper function to compute SHA256 hash of a string
static Hash computeSHA256(const std::string &input)
{
  unsigned char hash[SHA256_DIGEST_LENGTH];
  SHA256_CTX sha256;
  SHA256_Init(&sha256);
  SHA256_Update(&sha256, input.c_str(), input.size());
  SHA256_Final(hash, &sha256);

  std::stringstream ss;
  for (int i = 0; i < SHA256_DIGEST_LENGTH; i++)
  {
    ss << std::hex << std::setw(2) << std::setfill('0') << (int)hash[i];
  }
  return ss.str();
}

// Node methods
Hash Node::computeHash() const
{
  // Sort edges for canonical representation
  std::vector<std::pair<Hash, Hash>> sorted_edges = edges;
  std::sort(sorted_edges.begin(), sorted_edges.end());

  // Concatenate all hashes for content addressing
  std::stringstream ss;
  for (const auto &edge : sorted_edges)
  {
    ss << edge.first << edge.second;
  }

  return computeSHA256(ss.str());
}

YAML::Node Node::toYAML(NodeStore &store) const
{
  YAML::Node result;
  for (const auto &edge : edges)
  {
    YAML::Node edge_node;
    edge_node.push_back(edge.first);
    edge_node.push_back(edge.second);
    result.push_back(edge_node);
  }
  return result;
}

Node Node::fromYAML(const YAML::Node &node, NodeStore &store)
{
  Node result;
  if (!node.IsSequence())
  {
    throw std::runtime_error("Invalid YAML format: node must be a sequence");
  }

  for (const auto &edge_node : node)
  {
    if (!edge_node.IsSequence() || edge_node.size() != 2)
    {
      throw std::runtime_error("Invalid YAML format: edge must be a pair");
    }
    result.edges.emplace_back(
        edge_node[0].as<std::string>(),
        edge_node[1].as<std::string>());
  }
  return result;
}

// NodeStore methods
Hash NodeStore::store(const Node &node)
{
  Hash hash = node.computeHash();
  nodes[hash] = node;
  return hash;
}

const Node &NodeStore::get(const Hash &hash) const
{
  auto it = nodes.find(hash);
  if (it == nodes.end())
  {
    throw std::runtime_error("Node not found: " + hash);
  }
  return it->second;
}

bool NodeStore::has(const Hash &hash) const
{
  return nodes.find(hash) != nodes.end();
}

Hash NodeStore::empty()
{
  if (empty_hash.empty())
  {
    Node empty_node; // No edges
    empty_hash = store(empty_node);
  }
  return empty_hash;
}

Hash NodeStore::unit()
{
  if (unit_hash.empty())
  {
    Node unit_node;
    Hash e = empty();
    unit_node.edges.emplace_back(e, e);
    unit_hash = store(unit_node);
  }
  return unit_hash;
}

Hash NodeStore::match(const Hash &pattern, const Hash &input)
{
  // Get the pattern and input nodes
  const Node &pattern_node = get(pattern);
  const Node &input_node = get(input);

  // Create a new node to store matching edges
  Node result;

  // For each edge in the pattern, try to find matching edges in the input
  for (const auto &pattern_edge : pattern_node.edges)
  {
    for (const auto &input_edge : input_node.edges)
    {
      // Recursively match the components
      // If both match, add a new edge to the result
      if (pattern_edge == input_edge)
      {
        result.edges.push_back(input_edge);
      }
    }
  }

  // Store and return the resulting node
  return store(result);
}

void NodeStore::saveToFile(const std::string &filename) const
{
  YAML::Node root;

  // Store all nodes with their hashes as keys
  for (const auto &[hash, node] : nodes)
  {
    root[hash] = node.toYAML(*const_cast<NodeStore *>(this));
  }

  // Save to file
  std::ofstream fout(filename);
  if (!fout)
  {
    throw std::runtime_error("Could not open file for writing: " + filename);
  }
  fout << root;
}

void NodeStore::loadFromFile(const std::string &filename)
{
  // Clear existing nodes
  nodes.clear();
  empty_hash.clear();
  unit_hash.clear();

  // Load YAML
  YAML::Node root = YAML::LoadFile(filename);

  // Load all nodes
  for (const auto &pair : root)
  {
    Hash hash = pair.first.as<std::string>();
    Node node = Node::fromYAML(pair.second, *this);
    nodes[hash] = node;
  }
}