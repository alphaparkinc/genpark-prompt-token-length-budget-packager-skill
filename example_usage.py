from client import TokenBudgetPacker

samples = [
    {"id": "s1", "text": "Sample text " * 100},
    {"id": "s2", "text": "Another document with multiple paragraphs " * 80},
    {"id": "s3", "text": "Short prompt and answer."}
]
packed_bins = TokenBudgetPacker.pack_examples(samples, max_budget=1024)
print(f"Packed {len(samples)} examples into {len(packed_bins)} bins.")
for b in packed_bins:
    print(f"Bin {b['bin_id']}: {b['current_tokens']}/{b['max_budget']} tokens ({b['utilization_pct']}%)")
