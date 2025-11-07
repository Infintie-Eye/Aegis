"""
Example Usage Script for AI Mental Health Chatbot

This script demonstrates how to use the optimized CrewAI-based
mental health chatbot with various scenarios.
"""

import asyncio
import json
from main_orchestrator import MainOrchestrator


async def example_1_basic_support():
    """Example 1: Basic emotional support conversation"""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Basic Emotional Support")
    print("=" * 80 + "\n")

    # Initialize orchestrator for a user
    orchestrator = MainOrchestrator(user_id="user_demo_001")

    # User message
    user_message = "I've been feeling really down lately. Everything seems pointless and I don't enjoy things I used to love."

    print(f"USER: {user_message}\n")

    # Process message
    response = await orchestrator.process_message(
        message=user_message,
        session_context={"session_id": "session_001", "first_interaction": True}
    )

    # Display response
    print(f"CHATBOT: {response['response']}\n")
    print(f"Response Type: {response['response_type']}")
    print(f"Emotional Analysis: {json.dumps(response['emotional_analysis'], indent=2)}")
    print(f"Safety Status: {json.dumps(response['safety_status'], indent=2)}")

    # Display wellness suggestions if available
    if response.get('wellness_suggestions'):
        print(f"\nWellness Suggestions: {len(response['wellness_suggestions'])} categories available")

    return orchestrator


async def example_2_crisis_detection():
    """Example 2: Crisis detection and intervention"""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Crisis Detection and Intervention")
    print("=" * 80 + "\n")

    orchestrator = MainOrchestrator(user_id="user_demo_002")

    # Crisis message
    crisis_message = "I can't take this anymore. I feel like everyone would be better off without me. I don't see any point in going on."

    print(f"USER: {crisis_message}\n")
    print("⚠️  SYSTEM: Crisis indicators detected. Triggering immediate intervention...\n")

    # Process crisis message
    response = await orchestrator.process_message(
        message=crisis_message,
        session_context={"session_id": "session_002"}
    )

    # Display crisis response
    print(f"CHATBOT: {response['response']}\n")

    if response.get('crisis_level'):
        print(f"Crisis Level: {response['crisis_level']}/10")
        print(f"Urgency: {response.get('urgency', 'N/A')}")
        print(f"\nImmediate Resources:")
        for resource in response.get('immediate_resources', []):
            print(f"  - {resource['name']}: {resource['contact']}")

    return orchestrator


async def example_3_anxiety_support():
    """Example 3: Anxiety management with mindfulness recommendations"""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Anxiety Management Support")
    print("=" * 80 + "\n")

    orchestrator = MainOrchestrator(user_id="user_demo_003")

    # Anxiety message
    anxiety_message = "I have a presentation tomorrow and I'm so anxious I can't sleep. My heart is racing and I keep thinking about everything that could go wrong."

    print(f"USER: {anxiety_message}\n")

    # Process message
    response = await orchestrator.process_message(
        message=anxiety_message,
        session_context={"session_id": "session_003"}
    )

    # Display response
    print(f"CHATBOT: {response['response']}\n")
    print(f"Mental State Score: {response['mental_state']['overall_score']}/10")
    print(f"Primary Concerns: {', '.join(response['mental_state'].get('primary_concerns', []))}")

    # Display wellness suggestions
    if 'mindfulness' in response.get('wellness_suggestions', {}):
        print(f"\nMindfulness Exercises Recommended:")
        for exercise in response['wellness_suggestions']['mindfulness'][:2]:
            print(f"  - {exercise.get('name', 'Exercise')}: {exercise.get('duration', 'N/A')}")

    return orchestrator


async def example_4_depression_with_behavioral_activation():
    """Example 4: Depression support with behavioral activation"""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Depression Support with Behavioral Activation")
    print("=" * 80 + "\n")

    orchestrator = MainOrchestrator(user_id="user_demo_004")

    # Depression message
    depression_message = "I haven't left my bed in days. I have no energy or motivation to do anything. Everything feels so heavy."

    print(f"USER: {depression_message}\n")

    # Process message
    response = await orchestrator.process_message(
        message=depression_message,
        session_context={"session_id": "session_004"}
    )

    # Display response
    print(f"CHATBOT: {response['response']}\n")
    print(f"Therapeutic Guidance: {', '.join(response.get('therapeutic_guidance', []))}")

    # Display follow-up recommendations
    if response.get('follow_up_recommendations'):
        print(f"\nFollow-up Recommendations:")
        for rec in response['follow_up_recommendations']:
            print(f"  • {rec}")

    return orchestrator


async def example_5_multi_turn_conversation():
    """Example 5: Multi-turn conversation with personalization"""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Multi-Turn Conversation with Personalization")
    print("=" * 80 + "\n")

    orchestrator = MainOrchestrator(user_id="user_demo_005")

    # Conversation turns
    conversation = [
        "I'm struggling with stress at work. My boss is very demanding.",
        "I've tried taking breaks but it doesn't seem to help much.",
        "Maybe I need to look for a new job, but that seems overwhelming too."
    ]

    for i, message in enumerate(conversation, 1):
        print(f"\n--- Turn {i} ---")
        print(f"USER: {message}\n")

        response = await orchestrator.process_message(
            message=message,
            session_context={"session_id": "session_005", "turn": i}
        )

        print(f"CHATBOT: {response['response'][:200]}..." if len(
            response['response']) > 200 else f"CHATBOT: {response['response']}")
        print(f"Cache Efficiency: {response['interaction_metadata']['cache_efficiency']:.1f}%")

        # Small delay between turns
        await asyncio.sleep(0.5)

    # Show session insights
    print(f"\n--- Session Insights ---")
    print(f"Total Interactions: {response['interaction_metadata']['interaction_count']}")
    print(f"Session Insights: {json.dumps(response.get('session_insights', {}), indent=2)}")

    return orchestrator


async def example_6_wellness_recommendations():
    """Example 6: Comprehensive wellness recommendations"""
    print("\n" + "=" * 80)
    print("EXAMPLE 6: Comprehensive Wellness Recommendations")
    print("=" * 80 + "\n")

    orchestrator = MainOrchestrator(user_id="user_demo_006")

    # Message seeking holistic support
    message = "I want to improve my overall mental health. What can I do besides therapy?"

    print(f"USER: {message}\n")

    # Process message
    response = await orchestrator.process_message(
        message=message,
        session_context={"session_id": "session_006"}
    )

    # Display response
    print(f"CHATBOT: {response['response']}\n")

    # Display detailed wellness suggestions
    print("=== Wellness Recommendations ===\n")

    wellness = response.get('wellness_suggestions', {})

    if 'mindfulness' in wellness:
        print("🧘 MINDFULNESS ACTIVITIES:")
        for activity in wellness['mindfulness'][:2]:
            print(f"  • {activity.get('name')}")
            print(f"    Duration: {activity.get('duration')}")
            print(f"    Effectiveness: {activity.get('effectiveness_score', 'N/A')}")
        print()

    if 'physical_activities' in wellness:
        print("🏃 PHYSICAL ACTIVITIES:")
        for activity in wellness['physical_activities'][:2]:
            print(f"  • {activity.get('name')}")
            print(f"    Type: {activity.get('type')}")
            print(f"    Benefits: {', '.join(activity.get('benefits', []))}")
        print()

    if 'nutrition' in wellness:
        print("🍎 NUTRITION RECOMMENDATIONS:")
        for rec in wellness['nutrition'][:2]:
            print(f"  • {rec.get('meal')}")
            print(f"    Benefits: {', '.join(rec.get('benefits', []))}")
        print()

    return orchestrator


async def example_7_community_matching():
    """Example 7: Community and peer support matching"""
    print("\n" + "=" * 80)
    print("EXAMPLE 7: Community and Peer Support Matching")
    print("=" * 80 + "\n")

    orchestrator = MainOrchestrator(user_id="user_demo_007")

    # Message expressing loneliness
    message = "I feel so alone. No one understands what I'm going through."

    print(f"USER: {message}\n")

    # Process message
    response = await orchestrator.process_message(
        message=message,
        session_context={"session_id": "session_007"}
    )

    # Display response
    print(f"CHATBOT: {response['response']}\n")

    # Display community suggestions
    if response.get('community_suggestions'):
        print("=== Community Connection Suggestions ===\n")
        community = response['community_suggestions']

        print(f"Connection Priority: {community.get('connection_priority', 'N/A').upper()}\n")

        if community.get('support_groups'):
            print("SUPPORT GROUPS:")
            for group in community['support_groups'][:3]:
                print(f"  • {group.get('name', 'Support Group')}")
                print(f"    Focus: {group.get('focus', 'General Support')}")
                print(f"    Format: {group.get('format', 'Online/In-person')}")
            print()

    return orchestrator


async def example_8_progress_tracking():
    """Example 8: Progress tracking and insights"""
    print("\n" + "=" * 80)
    print("EXAMPLE 8: Progress Tracking and User Insights")
    print("=" * 80 + "\n")

    orchestrator = MainOrchestrator(user_id="user_demo_008")

    # Simulate multiple interactions
    messages = [
        "I'm feeling really depressed today.",
        "I tried the breathing exercise you suggested yesterday.",
        "I'm feeling a bit better after doing the exercise.",
        "Thanks for your support. I think I'm making progress."
    ]

    print("Simulating conversation over multiple sessions...\n")

    for i, msg in enumerate(messages, 1):
        await orchestrator.process_message(
            message=msg,
            session_context={"session_id": f"session_008_{i}"}
        )
        print(f"✓ Processed message {i}/{len(messages)}")

    # Get progress report
    print("\n=== User Progress Report ===\n")
    progress_report = await orchestrator.get_user_progress_report()

    print(f"Engagement Metrics:")
    print(f"  Total Interactions: {progress_report['engagement_metrics']['total_interactions']}")
    print(f"  Cache Efficiency: {progress_report['engagement_metrics']['average_cache_efficiency']:.1f}%")

    print(f"\nTherapeutic Progress:")
    insights = progress_report.get('therapeutic_progress', {})
    if insights.get('primary_needs'):
        print(f"  Primary Needs: {', '.join(insights['primary_needs'])}")

    return orchestrator


async def main():
    """Run all examples"""
    print("\n" + "=" * 80)
    print(" AI MENTAL HEALTH CHATBOT - COMPREHENSIVE EXAMPLES")
    print(" Using CrewAI Framework with Google Gemini Pro")
    print("=" * 80)

    examples = [
        ("Basic Emotional Support", example_1_basic_support),
        ("Crisis Detection", example_2_crisis_detection),
        ("Anxiety Management", example_3_anxiety_support),
        ("Depression Support", example_4_depression_with_behavioral_activation),
        ("Multi-Turn Conversation", example_5_multi_turn_conversation),
        ("Wellness Recommendations", example_6_wellness_recommendations),
        ("Community Matching", example_7_community_matching),
        ("Progress Tracking", example_8_progress_tracking),
    ]

    print("\nAvailable Examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")

    print("\nRunning Example 1 (Basic Emotional Support)...")
    print("To run other examples, uncomment them in the main() function or run individually.\n")

    # Run Example 1 by default
    await example_1_basic_support()

    # Uncomment to run other examples:
    # await example_2_crisis_detection()
    # await example_3_anxiety_support()
    # await example_4_depression_with_behavioral_activation()
    # await example_5_multi_turn_conversation()
    # await example_6_wellness_recommendations()
    # await example_7_community_matching()
    # await example_8_progress_tracking()

    print("\n" + "=" * 80)
    print(" Examples completed successfully!")
    print(" Modify this script to run specific examples or create your own scenarios.")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    # Run the examples
    asyncio.run(main())
