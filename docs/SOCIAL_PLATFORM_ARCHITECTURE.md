# Social Platform Architecture

Facebook, Instagram, LINE/LINE OA and TikTok are optional adapters behind one provider contract. Platform-specific behavior stays inside adapters.

Every publish/send operation carries trace, task, employee, agent, integration and action identifiers and passes authorization, platform policy and idempotency controls.
