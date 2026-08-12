# Workload, capacity and scheduling

Track active_tasks, queued_tasks, completed_tasks, failed_tasks, capacity, and utilization. Overload → reassign, queue, or escalate.

Controls: max_concurrent_tasks, max_parallel_agents, max_workflow_depth, max_team_size. Scheduling supports priority, deadline, scheduled_time, dependencies, and availability. Scheduling cannot bypass authorization.

Unavailable employee → detect → pause → find backup → permission check → transfer context → resume. No backup → human escalation.