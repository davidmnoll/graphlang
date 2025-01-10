#include <gtest/gtest.h>
#include "../include/node_store.hpp"
#include <fstream>

class NodeStoreTest : public ::testing::Test
{
protected:
  NodeStore store;

  void SetUp() override
  {
    // Called before each test
  }

  void TearDown() override
  {
    // Called after each test
  }
};

TEST_F(NodeStoreTest, EmptyNode)
{
  Hash empty = store.empty();
  const Node &node = store.get(empty);
  EXPECT_TRUE(node.edges.empty());
}

TEST_F(NodeStoreTest, UnitNode)
{
  Hash unit = store.unit();
  const Node &node = store.get(unit);
  EXPECT_EQ(node.edges.size(), 1);
  EXPECT_EQ(node.edges[0].first, store.empty());
  EXPECT_EQ(node.edges[0].second, store.empty());
}

TEST_F(NodeStoreTest, StoreAndRetrieve)
{
  Node test_node;
  test_node.edges = {
      {store.empty(), store.unit()},
      {store.unit(), store.empty()}};

  Hash hash = store.store(test_node);
  EXPECT_TRUE(store.has(hash));

  const Node &retrieved = store.get(hash);
  EXPECT_EQ(retrieved.edges.size(), 2);
  EXPECT_EQ(retrieved.edges, test_node.edges);
}

TEST_F(NodeStoreTest, YAMLSerialization)
{
  // Create a test node
  Node test_node;
  test_node.edges = {
      {store.empty(), store.unit()},
      {store.unit(), store.empty()}};
  Hash original_hash = store.store(test_node);

  // Save to YAML
  const std::string test_file = "test_store.yaml";
  store.saveToFile(test_file);

  // Create new store and load
  NodeStore new_store;
  new_store.loadFromFile(test_file);

  // Verify contents
  EXPECT_TRUE(new_store.has(original_hash));
  const Node &loaded_node = new_store.get(original_hash);
  EXPECT_EQ(loaded_node.edges, test_node.edges);

  // Cleanup
  std::remove(test_file.c_str());
}

TEST_F(NodeStoreTest, BasicPatternMatching)
{
  // Create pattern: [(E,U)]
  Node pattern;
  pattern.edges = {{store.empty(), store.unit()}};
  Hash pattern_hash = store.store(pattern);

  // Create input: [(E,U), (U,E)]
  Node input;
  input.edges = {
      {store.empty(), store.unit()},
      {store.unit(), store.empty()}};
  Hash input_hash = store.store(input);

  // Match should find the common edge
  Hash result_hash = store.match(pattern_hash, input_hash);
  const Node &result = store.get(result_hash);
  EXPECT_EQ(result.edges.size(), 1);
  EXPECT_EQ(result.edges[0].first, store.empty());
  EXPECT_EQ(result.edges[0].second, store.unit());
}