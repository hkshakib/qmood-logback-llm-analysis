# LLM Comparison Summary

ChatGPT gave a balanced and cautious explanation of the metric trends. It described the decrease in class count, the stable coupling values, and the trade-off between later functionality gains and lower understandability. It was useful for a simple academic explanation because it did not overstate the results.

Gemini gave the most detailed metric-specific discussion. It used concrete values from the tables and connected them to size reduction, complexity, cohesion, flexibility, and understandability. It was useful for report discussion, although some wording was more interpretive than the metrics alone can fully prove.

DeepSeek explained the evolution in clear phases. It separated the versions into decline, partial recovery, and final decline periods, which makes the trend easy to follow. It was useful for summarizing the quality evolution, especially the trade-off between functionality and maintainability-related scores.

Overall, all three models understood the provided metric tables and gave useful qualitative interpretations. ChatGPT was the most cautious, Gemini was the most detailed, and DeepSeek was the clearest for phase-based trend explanation. None of the models should be treated as source-code reviewers because they used only the provided metrics and did not inspect the Logback source code directly.

This comparison is qualitative and manual. The LLM outputs depend on the prompt wording, the metric tables, and each model's explanation style. The responses should support the project discussion, but they should not replace the CK metrics or the QMOOD-inspired calculations.
