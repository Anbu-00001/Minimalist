"""GBNF grammars for constrained local generation (llama.cpp).

Used ONLY for classification/extraction outputs — research shows constrained
decoding degrades reasoning tasks 10-30% while helping classification
(Tam et al. 2408.02442), so math/logic/code/summaries stay free-form.
See research/VERDICTS.md V5.
"""

# Vendored verbatim from ggml-org/llama.cpp grammars/json.gbnf (MIT license),
# fetched 2026-07-07. Guarantees well-formed JSON output; keys/content remain
# the model's job (our verifier checks those).
JSON_GBNF = r'''root   ::= object
value  ::= object | array | string | number | ("true" | "false" | "null") ws

object ::=
  "{" ws (
            string ":" ws value
    ("," ws string ":" ws value)*
  )? "}" ws

array  ::=
  "[" ws (
            value
    ("," ws value)*
  )? "]" ws

string ::=
  "\"" (
    [^"\\\x7F\x00-\x1F] |
    "\\" (["\\bfnrt] | "u" [0-9a-fA-F]{4}) # escapes
  )* "\"" ws

number ::= ("-"? ([0-9] | [1-9] [0-9]{0,15})) ("." [0-9]+)? ([eE] [-+]? [0-9] [1-9]{0,15})? ws

# Optional space: by convention, applied in this grammar after literal chars when allowed
ws ::= | " " | "\n" [ \t]{0,20}
'''

# Forces exactly one sentiment label token — used for the cheap second-read
# agreement check, never for the shipped answer (whose format the task dictates).
SENTIMENT_LABEL_GBNF = 'root ::= "positive" | "negative" | "neutral" | "mixed"'
