# Valid Palindrome — lesson plan

> **Workflow:** Fill this file first. The lesson HTML is generated only
> after this plan is reviewed.

## Metadata
- **Slug:** `valid-palindrome`
- **LC #:** 125
- **Difficulty:** Easy
- **Topic:** Strings & Two Pointers
- **Archetype:** `two_pointer` (squeeze from both ends after filtering)

## 1. Clarifying questions (§0)

1. **Q:** Which characters should we ignore?
   **A:** Non-alphanumeric characters (letters and digits only). Spaces, punctuation, symbols all ignored.
   **Unlock:** We can skip ahead without storing; only compare alphanumeric chars.

2. **Q:** Is comparison case-sensitive?
   **A:** No. 'A' and 'a' are treated as the same.
   **Unlock:** Normalize each character on-the-fly; no pre-processing needed.

3. **Q:** What if the string has only non-alphanumeric characters?
   **A:** It is a valid palindrome (vacuously true).
   **Unlock:** After filtering, an empty string is a palindrome.

4. **Q:** Can we use O(n) extra space?
   **A:** Better not to. A clean solution skips non-alphanumeric in-place with O(1) auxiliary space.
   **Unlock:** Two pointers advance inward; no cleaned copy needed.

## 2. Kernel paragraph (§1)

Use two pointers, left at the start and right at the end. Advance left and right inward, skipping non-alphanumeric characters. At each step, compare the alphanumeric characters at left and right (case-insensitive). If they differ, return false. If pointers meet or cross, return true. This achieves O(n) time with O(1) space and no pre-processing.

## 3. Brute force intuition (§2)

Create a cleaned string by keeping only alphanumeric characters (lowercased). Then check if the cleaned string equals its reverse. O(n) time, O(n) space (the cleaned string).

## 4. Translations (§3)

**Translation 1 — Brute force (cleanup then compare).**
Iterate through and keep only alphanumeric characters (lowercased) in a new string. Compare the string to its reverse. O(n) time, O(n) space.
→ `O(n) space used`

**Translation 2 — Two-pointer with on-the-fly filtering (taught).**
Use left and right pointers. Skip non-alphanumeric at each end. Compare alphanumeric chars (case-insensitive). O(n) time, O(1) space, no pre-processing.
→ `O(1) space; optimal.`

## 5. Algorithm in plain English (§4)

1. **Initialize** left = 0, right = len(s) - 1.
2. **Loop** while left < right:
   - Skip non-alphanumeric: increment left until s[left] is alphanumeric.
   - Skip non-alphanumeric: decrement right until s[right] is alphanumeric.
   - Compare s[left] and s[right] (both lowercased). If not equal, return false.
   - Move left forward, right backward.
3. **Return true** if loop completes.

## 6. Examples for code viz + dry run (§6, §7)

**Fast example:** `s = "a."` → **true** (~4 steps)
- left=0 ('a', alphanumeric), right=1 ('.', not alphanumeric)
- Right skips and moves out of bounds; loop exits.
- Return true.

**Slow example:** `s = "A man, a plan, a canal: Panama"` → **true** (~14 steps)
- Initialize left=0, right=29
- Step 1: Compare 'A' (→'a') at left=0 and 'a' at right=29 → match. left=1, right=28.
- Step 2: Skip left=1 (' '), advance to left=2 ('m'). Compare 'm' at left=2 and 'm' at right=28 → match. left=3, right=27.
- Continue matching pairs: a=a, n=n, a=a, p=p, l=l, a=a, n=n, a=a, c=c.
- Eventually left and right converge; return true.

**Dry run example:** `s = "0P"` → **false** (~2 steps)
- left=0 ('0', alphanumeric), right=1 ('P', alphanumeric)
- Compare '0' and 'p' (lowercased) → not equal. Return false.

## 7. Corner cases (§8)

1. **Empty string `""`:** No chars; left=0, right=-1; loop doesn't run. Return true.
2. **Single char `"a"`:** left=0, right=0; left < right is false; loop doesn't run. Return true.
3. **All non-alphanumeric `"!@#$%"`:** Both pointers skip to out-of-bounds; loop exits. Return true.
4. **Mixed case `"Aa"`:** left='A' → 'a', right='a'; they match. Return true.
5. **Mismatch at edges `"ab"`:** left='a', right='b'; no match. Return false.

## 8. Approaches comparison (§10)

**Approach 1 — Two-pointer with on-the-fly filtering (taught).**
Maintain left and right pointers, skip non-alphanumeric, compare case-insensitively. O(n) time, O(1) space, no modification. Optimal for this problem.

**Approach 2 — Brute force (cleanup then compare).**
Build a cleaned, lowercased string, then compare to its reverse. Simple and intuitive. O(n) time, O(n) space.

**Approach 3 — Regex + reverse.**
Use regex to remove non-alphanumeric, then compare with reversed string. Concise. O(n) time, O(n) space (for regex result).

## 9. Take home (§12)

LC 680 — Valid Palindrome II — allow one character deletion; introduces recovery strategy.

LC 1332 — Remove Palindromic Subsequences — combine palindrome checking with subsequence logic.

LC 1216 — Valid Palindrome III — use DP to check if string is palindrome after removing at most k characters.

## 10. Python verification (BEFORE writing HTML)

```python
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        # Skip non-alphanumeric on the left
        while left < right and not s[left].isalnum():
            left += 1
        # Skip non-alphanumeric on the right
        while left < right and not s[right].isalnum():
            right -= 1
        # Compare (case-insensitive)
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True

# Test cases
test_cases = [
    ("a.", True),
    ("A man, a plan, a canal: Panama", True),
    ("0P", False),
    ("", True),
    ("a", True),
    ("!@#$%", True),
    ("Aa", True),
    ("ab", False),
]

for s, expected in test_cases:
    result = is_palindrome(s)
    status = "✓" if result == expected else "✗"
    print(f"{status} is_palindrome({repr(s)}) = {result} (expected {expected})")
```

Running trace:
```
✓ is_palindrome('a.') = True (expected True)
✓ is_palindrome('A man, a plan, a canal: Panama') = True (expected True)
✓ is_palindrome('0P') = False (expected False)
✓ is_palindrome('') = True (expected True)
✓ is_palindrome('a') = True (expected True)
✓ is_palindrome('!@#$%') = True (expected True)
✓ is_palindrome('Aa') = True (expected True)
✓ is_palindrome('ab') = False (expected False)

All test cases passed.
```
