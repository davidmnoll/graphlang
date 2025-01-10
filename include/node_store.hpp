#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <yaml-cpp/yaml.h>

// Forward declaration
class NodeStore;

// Hash type for content addressing
using Hash = std::string;

class Node
{
public:
  // A node is just a list of pairs of node references
  std::vector<std::pair<Hash, Hash>> edges;

  // Compute content hash of this node
  Hash computeHash() const;

  // YAML serialization
  YAML::Node toYAML(NodeStore &store) const;
  static Node fromYAML(const YAML::Node &node, NodeStore &store);
};

class NodeStore
{
public:
  // Core operations
  Hash store(const Node &node);
  const Node &get(const Hash &hash) const;
  bool has(const Hash &hash) const;

  // Special nodes
  Hash empty(); // Empty node (E) = []
  Hash unit();  // Unit node (U) = [(E,E)]

  // Pattern matching
  Hash match(const Hash &pattern, const Hash &input);

  // YAML serialization
  void saveToFile(const std::string &filename) const;
  void loadFromFile(const std::string &filename);

private:
  std::unordered_map<Hash, Node> nodes;

  // Cache for special nodes
  Hash empty_hash;
  Hash unit_hash;
};