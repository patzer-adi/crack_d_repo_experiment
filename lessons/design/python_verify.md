# Cross-cutting — Python algorithm verification

## Principle (from v2 §26)

**Verify algorithm correctness with a Python trace before writing any HTML.**

For every problem, run a Python simulation of the algorithm against all planned examples before writing the step generator. Print every variable at every step. Verify the output matches expected. This catches logic bugs — especially diff counter inversions — before they are embedded in hundreds of lines of JS. A bug in the step generator produces subtly wrong narration that is very hard to find later.

## Standard pattern

```python
def verify(nums, expected):
    nums = sorted(nums)
    n = len(nums)
    result = []
    print(f"Input (sorted): {nums}")
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i-1]:
            print(f"  i={i}: skip dup")
            continue
        L, R = i + 1, n - 1
        while L < R:
            s = nums[i] + nums[L] + nums[R]
            print(f"  i={i} L={L} R={R} sum={s}")
            if s < 0:
                L += 1
            elif s > 0:
                R -= 1
            else:
                result.append([nums[i], nums[L], nums[R]])
                while L < R and nums[L] == nums[L+1]: L += 1
                while L < R and nums[R] == nums[R-1]: R -= 1
                L += 1; R -= 1
    print(f"Result: {result}")
    print(f"Expected: {expected}")
    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))

verify([-1,0,1,2,-1,-4], [[-1,-1,2], [-1,0,1]])
verify([0,0,0,0], [[0,0,0]])
verify([1,2,3], [])
```

## Always print what the algorithm returns

Then decide if that's the right example to use — **do not** write a test with an expected value from memory. Memory is wrong about edge cases more often than the algorithm is.

## When to re-verify

- Whenever the algorithm changes.
- Whenever an example is added.
- Whenever you change the dry-run example switcher's examples — they must match the Python trace exactly.

## Where this fits in the workflow

After §0 (Clarifying questions) is decided and before §2 (Brute force) animation is implemented. The Python verifier output is the source of truth for both the `cvGen` and `drGen` step generators.

In Phase 2 of PLAN-011 (the renderer), this verifier becomes a hard gate: `scripts/verify_algorithm.py` will read `code.python` from `spec.json` and refuse to render if any example fails.
