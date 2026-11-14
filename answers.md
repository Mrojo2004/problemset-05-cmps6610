# CMPS 6610 Problem Set 05
## Answers


**Name:** Marcus Rojo


## 1. Shortest shortest paths


**1b) (4 pts)** Work and span 
My algorithm is Dijkstra's, but the heap stores weight and number of edges instead of just weight. When two paths have the same weight, the one with fewer edges will come out first. It is also important to note that this doesn't change the cost, as comparing the pairs is still O(1).

 Work: $O(|E| \log |E|)$. Each edge causes at most one push and one pop on the heap, and each heap operation costs $O(\log |E|)$. This visited check also costs O(1) per pop.
 Span: $O(|E| \log |E|)$. The vertices are settled one at a time in priority order, and each step depends on the previous step. This means that the algorithm is sequential. 


## 2. Expression Trees


**2a) (3 pts)** Expression tree algorithm with work and span
I would scan the expression left to right with two stacks. The two stacks include an operand stack of subtrees and an operator stack. 
- On a literal, push a leaf node onto the operand stack.
- On "(" or an operator, push it onto the operator stack.
- On ")", pop operators until the matching "(" is reached. For each operator popped, pop two subtrees $L, R$ and push a new node "op(L, R)". Including a unary minus takes one subtree.
- At the end, apply any remaining operators the same way as described above. With that, the single subtree remaining on the operand stack is $T_E$. 

Each token is pushed and popped at most once, and building each node costs O(1).
- Work: $O(n)$
- Span: $O(n)$, because the stack-based scan is inherently sequential.

**2b) (2 pts)** Corresponding arithmetic expression work and span?
Evaluate bottom-up: a leaf returns its value (looking up variables in a table). An internal node evaluates its two children in parallel and then applies its operator.
- Work: $O(n)$, because each node is visited once at O(1) cost.
- Span: $O(h)$, where h is the tree height. That is $O(\log n)$ for a balanced tree and $O(n)$ in the worst case, a "linear" expression like ((((a+b)+c)+d)+...).

**2c) (2 pts)** work/span to update a previously computed value
First, I would need to store the computed value at each node. When one variable changes, only the nodes on the path from the leaf to the root will change. Then, I'd recompute each node on that path from its updated child and its sibling's cached value. 
- Work and span: $O(h)$, which is $O(\log n)$ if the tree is balanced and $O(n)$ in the worst case. The path is sequential, so span equals work.
- If the variable appears in m leaves, the cost is $O(m \cdot h)$ work. The paths can be updated in parallel up to where they merge, which gives $O(h)$span.


## 3. Improving Dijkstra


**3a) (2 pts)** Maximum depth of a $d$-ary heap
A $d$-ary heap with $n$ elements is a complete $d$-ary tree, and each level holds $d$ times as many nodes as the one above. This means that the depth is $O(\log_d n)$.


**3b) (3 pts)** Work done by `delete-min` and `insert` operations in a $d$-ary heap.
- insert: $O(\log_d n)$. The new element moves up one level at a time, comparing only with its parent.
- delete-min: $O(d \log_d n)$. The element sifts down. At each level, finding the smallest of the $d$ children takes $d-1$ comparisons, plus one comparison against the element itself, across $O(\log_d n)$ levels.


**3c) (3 pts)** New bound on the work for Dijkstra's using $d$-ary heap 
Dijkstra does $|V|$ delete-mins (one per vertex) and up to $|E|$ inserts (one per edge).

So:

$$W = O\big(|V| \cdot d \log_d |V| + |E| \log_d |V|\big)$$

The first term is delete-min and the second term is insert. 

**3d) (3 pts)** What value of $d$ yields an overall running time of $O(|E|)$?
 Choose $d = |V|^{\epsilon}$. Then $\log_d |V| = \frac{1}{\epsilon}$, which is a constant. 
 
 Plugging into 3c:

$$O\big(|V| \cdot |V|^{\epsilon} + |E|\big) = O\big(|V|^{1+\epsilon} + |E|\big) = O(|E|)$$

since $|E| = |V|^{1+\epsilon}$.

## 4. All-pairs shortest paths using Dynamic Programming

**4a) (2 pts)** Consider the following graph with 3 vertices.
I treated the edges as two-way and counted only paths that don't repeat a vertex. $\mathit{APSP}(i,i,k) = 0$ for every k. The tables are also symmetric. 

**k = 0** (only vertex 0 can be used in between them)

| | 0 | 1 | 2 |
|---|---|---|---|
| **0** | 0 | -2 | 2 |
| **1** | -2 | 0 | 0 |
| **2** | 2 | 0 | 0 |

**k = 1** (vertices 0 and 1 can be used here)

| | 0 | 1 | 2 |
|---|---|---|---|
| **0** | 0 | -2 | -1 |
| **1** | -2 | 0 | 0 |
| **2** | -1 | 0 | 0 |

**k = 2**: it is the same as k = 1. This shows that going through vertex 2 never helps: 0→2→1 = 3 > -2. So $\mathit{APSP}(\cdot,\cdot,2) = \mathit{APSP}(\cdot,\cdot,1)$.

**4b) (3 pts)** Relationship between $\mathit{APSP}(i, j, 1)$ and
$\mathit{APSP}(i, j, 2)$. Can you write $\mathit{APSP}(i, j, 2)$ in
terms of $\mathit{APSP}(i, j, 0)$ and $\mathit{APSP}(i, j, 1)$ only?
Going from k=1 to k=2 only allows vertex 2 as a stop in between. So the best path either doesn’t use vertex 2, or it goes i → 2 → j:

$$\mathit{APSP}(i,j,2) = \min\big(\mathit{APSP}(i,j,1),\ \mathit{APSP}(i,2,1) + \mathit{APSP}(2,j,1)\big)$$

In this graph, vertex 2 never helps, so APSP(i,j,2) = APSP(i,j,1).

**4c) (3 pts)** Generalize your observation from b) above to give an optimal substructure property for $\mathit{APSP}(i, j, k).$
$$\mathit{APSP}(i,j,k) = \min\big(\mathit{APSP}(i,j,k-1),\ \mathit{APSP}(i,k,k-1) + \mathit{APSP}(k,j,k-1)\big)$$

The shortest path either skips vertex k (the first term), or it goes through k. If it goes through k, the two halves i→k and k→j are the shortest paths that use only vertices up to k-1 (the second term).

**4d) (3 pts)** How many distinct subproblems will be computed from scratch, and
what is the resulting work of this dynamic programming algorithm?
There are $n$ choices each for i, j and k, so there are $n^3$ subproblems. Each one is a min of two values, which means it's O(1) work. 

Total work: $O(n^3)$.

**4e) (3 pts)** Compare the work of this algorithm against that of just running
Dijkstra $n$ times. Is our dynamic programming algorithm better than this?
Running Dijkstra n times costs $O(n|E|\log|E|)$.

Dense graph ($|E| \approx n^2$): Dijkstra is $O(n^3 \log n)$, meaning the DP’s $O(n^3)$ is better.
Sparse graph ($|E| \approx n$): Dijkstra is $O(n^2 \log n)$, which leads me to believe that Dijkstra is better.

The DP also works with negative edge weights, which Dijkstra can’t handle.

## 5. Spanning trees

**5a) (3 pts)** Is a solution to MST guaranteed to be a solution to MMET? Why or why not?
Yes, every MST solution is guaranteed to be a solution to MMET.

For example, let's say that the MST $T$ has the heaviest edge $e$ with weight $w$, and some other spanning tree has all edges lighter than $w$. Then we remove $e$ from $T$, which splits the graph into two pieces. It must also be noted that the other tree must have an edge $e'$ connecting those two pieces, and $w(e') < w$. Swapping $e$ out for $e'$ gives a spanning tree that is lighter than $T$. However. that’s impossible because $T$ is the MST, meaning that no such tree exists, and that confirms that $T$’s heaviest edge is as small as possible.

The converse is false because an MMET does not need to be an MST, as it only constrains the maximum edge. For example, in a triangle with edge weights 1, 2, 2 plus a fourth vertex attached by an edge of weight 5, any spanning tree must use the weight-5 edge. Every spanning tree is then an MMET, including any spanning tree that may have a larger total weight.

**5b) (2 pts)** Suppose that the optimal solution to MST is impossible to use for some reason. Describe an algorithm to instead find the next best tree (pseudo-code or English is fine). That is, return the tree with the next lowest weight. 

An algorithm to find the next best tree.
The MST $T$ has $|V| - 1$ edges. 
For each edge $e$ in $T$:
1. Remove $e$ from the graph.
2. Run Kruskal’s algorithm on what’s left to get the best tree without $e$.

After trying every edge, return the lightest of these trees.

This works because the second-best tree must be missing at least one edge of $T$, as otherwise it would be $T$. By  trying every possible missing edge, this algorithm is simple and is guaranteed to find it.

**5c) (2 pts)** What is the work of your algorithm?
Kruskal runs $|V| - 1$ times, at $O(|E| \log |E|)$ each.
- Work: $O(|V| \cdot |E| \log |E|)$.

