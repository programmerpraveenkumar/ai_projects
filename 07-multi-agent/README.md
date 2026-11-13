# Multi-Agent

A simple supervisor pattern:

User
  -> Supervisor
      -> Researcher: finds relevant content
      -> Generator: creates MCQs
      -> Validator: checks quality
      -> Supervisor decides next step
      -> Saver

Do not use multiple agents unless separation of responsibilities provides a real benefit. For this learning project, the main lesson is role separation and orchestration.
