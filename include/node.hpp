#pragma once
#include <string>
#include <vector>
#include <yaml-cpp/yaml.h>
#include "node_store.hpp"

class Node
{
public:
  // Data structure to hold node properties
  struct NodeData
  {
    std::string name;

    // YAML serialization
    YAML::Node toYAML() const;
    static NodeData fromYAML(const YAML::Node &node);
  };

  // Node properties
  NodeData data;
  std::vector<std::pair<Hash, Hash>> children;

  // Compute content hash of this node
  Hash computeHash() const;

  // YAML serialization
  YAML::Node toYAML() const;
  static Node fromYAML(const YAML::Node &node);

private:
  // Helper function to compute SHA-256 hash
  static Hash computeSHA256(const std::string &input);
};