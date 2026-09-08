---
name: test-integration
description: Use when asked for integration tests, or to replace brittle mocks with fakes, across any software architecture layer (backends, mobile apps, desktop systems, service modules) — verifying data flowing across components, persistent storage updates, reactive event streams or message brokers, or asynchronous thread boundaries. Not for isolated unit tests of a single class, or tests that name no kind.
---

# Test Integration

## Overview

Integration tests verify that two or more concrete architectural components interact, exchange data, and manage state boundaries correctly. Unlike unit tests, integration tests minimize mocking to guarantee that reactive pipelines, data structures, and multi-layered contracts do not break when components collaborate in a real environment.

**The project's rules and the surrounding file come first — read what `AGENTS.md` loads for this work, if you haven't.**

---

## Key Principles & Structure Rules

| Rule | Detail |
|------|--------|
| **Test Collaboration, Not Isolation** | Pass real implementations of components wherever possible. Connect layers exactly as they are wired in production (e.g., `Service` + `Repository` + `Database`). |
| **Assert State and Side-Effects** | Do not verify internal method call invocations or line-by-line execution patterns. Assert the actual end-state mutations, persistent data changes, or downstream emitted events. |
| **Fakes Over Mocks** | For external system boundaries (third-party APIs, hardware layers, network protocols), use lightweight, predictable **Fakes** or in-memory systems rather than a mocking library. |
| **Verify Stream Lifecycle** | Test continuous streams (asynchronous flows, message queues, reactive events) to ensure data survives across layer boundaries without memory leaks, dropping frames, or stalling. |
| **Isolate via File Suffix** | Keep integration tests in a separate file using the strict `IntegrationTest` postfix (e.g., `ProductViewModelIntegrationTest.kt`). They may share a directory with your unit tests for local JVM discovery, but must never mix individual test methods within the same file. |
| **Table Tests for Workflows** | Use when verifying identical integrations across varying input matrices. Prefer distinct test functions with clean helper inputs if failures point to distinct data structural breaks. |
| **Avoid Configuration Bleed** | Keep the setup localized to the exact components under test. Avoid leaking unnecessary framework configs, system environments, or database states into tests that do not use them. |
| **No Backdoors or Reflection** | Drive system state changes strictly via public APIs, shared fakes, or explicit execution triggers. Testing structures must not rely on private internal references. |
| **Given/When/Then Comments** | In every integration test body to clearly mark configuration, execution, and state assertions. |
| **When/Then Naming** | Use descriptive, concise names capturing the architectural integration behavior and structural changes being checked. |

---

## Tech Stack

Check this project's actual configured stack for what it uses — this skill doesn't claim a
specific framework. The template below is written with JUnit5-style annotations (`@BeforeEach`/`@AfterEach`)
as a concrete illustration; adapt the annotations to match the real framework (JUnit4's
`@Before`/`@After`, pytest fixtures, Jest's `beforeEach`) — the principles in the table above are
what actually matters and don't change with the annotation syntax.

---

## Template

```text
// File 1: ProductViewModelTest.kt            <-- Isolated Unit Tests using Mocks
// File 2: ProductViewModelIntegrationTest.kt <-- Co-located Integration Tests using Fakes

class ExampleComponentIntegrationTest {
    
    // Concrete integration components (Real classes or Fakes)
    private var fakeExternalGateway
    private var realRepository
    private var realOrchestrator

    @BeforeEach
    fun setup() {
        // 1. Initialize external boundaries using specialized Fakes
        fakeExternalGateway = FakeExternalGateway()
        
        // 2. Chain real production dependencies together exactly like production
        realRepository = RealRepository(fakeExternalGateway)
        realOrchestrator = RealOrchestrator(realRepository)
    }

    @AfterEach
    fun tearDown() {
        // Clear or wipe memory cache state inside your Fakes if reused
        fakeExternalGateway.clear()
    }
    
    @Test
    fun `when external data arrives then orchestrator state holds every item`() {
        // Given
        val incomingData = ["DataPayloadA", "DataPayloadB"]
        
        // When - Action occurs at the low-level data source layer boundary
        fakeExternalGateway.simulateIncomingData(incomingData)
        realOrchestrator.triggerProcessing()

        // Then - Assert the pipeline accurately propagates up to the highest layer
        val finalState = realOrchestrator.getCurrentState()
        assertTrue(finalState is State.Success)
        assertEquals(2, finalState.items.size)
    }

    @Test
    fun `when gateway fails then orchestrator state is error with its message`() {
        // Given
        fakeExternalGateway.simulateSystemFailure(RuntimeException("Connection dropped"))

        // When
        realOrchestrator.triggerProcessing()

        // Then
        val finalState = realOrchestrator.getCurrentState()
        assertTrue(finalState is State.Error)
        assertEquals("Connection dropped", finalState.errorMessage)
    }
}
```

---

## What to Test

**Boundary Handoffs** — Verify data model translation, caching logic, and validation when data flows between completely different architectural layers (e.g., Presentation layer to Domain layer, Domain layer to Database).

**Reactive Streams and Pipelines** — Ensure event pipelines match across layers. Confirm that if a higher layer cancels an operation or changes system constraints, lower-level components close data flows or release resource locks gracefully without hanging.

**Threading and Concurrency Bridges** — Check that thread-shifting transitions (e.g., background worker thread to main thread) happen safely across components without throwing race condition errors or dropping concurrent payload updates.

**Error Propagation and Self-Healing** — Test how the combined system behaves when a low-level boundary fails. Ensure the intermediate components map raw infrastructure errors into predictable domain data or safe fallbacks rather than crashing.

**State Divergence** — Test edge conditions where different modules have conflicting states (e.g., a network source registers a successful transaction, but local persistence fails to update). Verify that the system handles these edge cases cleanly.
