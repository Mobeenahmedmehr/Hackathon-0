"""
LinkedIn agent for creating LinkedIn posts in the AI Employee system.
"""

from pathlib import Path
from .base_agent import BaseAgent


class LinkedInAgent(BaseAgent):
    """
    Agent responsible for creating LinkedIn posts.
    """

    def __init__(self):
        super().__init__()
        self.drafts_dir = Path("Drafts")

    def execute(self, plan_data):
        """
        Execute LinkedIn post creation based on the plan data.

        Args:
            plan_data (dict): Data containing LinkedIn post information

        Returns:
            Result of the execution
        """
        try:
            return self.create_post(plan_data)
        except Exception as e:
            return self.handle_error(e, "execute")

    def create_post(self, plan_data):
        """
        Create a LinkedIn post based on the provided plan data.

        Args:
            plan_data (dict): Data containing post creation information

        Returns:
            dict: Result of the post creation operation
        """
        try:
            task_id = plan_data.get('task_id', 'unknown')
            content = plan_data.get('content', '')
            hashtags = plan_data.get('hashtags', [])
            title = plan_data.get('title', 'LinkedIn Post')

            # Format the post content
            post_content = f"""# {title}

{content}

"""

            if hashtags:
                hashtag_str = ' '.join([f"#{tag.strip('#')}" for tag in hashtags])
                post_content += f"\n{hashtag_str}\n"

            post_content += f"""
---
Post draft created at: {self._get_timestamp()}
Task ID: {task_id}
"""

            # Ensure drafts directory exists
            self.drafts_dir.mkdir(exist_ok=True)

            # Save post draft as markdown file
            post_file = self.drafts_dir / f"linkedin_post_{task_id}.md"
            with open(post_file, 'w', encoding='utf-8') as f:
                f.write(post_content)

            self.log_action("create_post", {
                "task_id": task_id,
                "title": title,
                "hashtags": hashtags,
                "post_file": str(post_file)
            })

            return {
                "success": True,
                "post_file": str(post_file),
                "message": f"LinkedIn post draft saved to {post_file}"
            }
        except Exception as e:
            return self.handle_error(e, "create_post")

    def _get_timestamp(self):
        """Helper method to get current timestamp."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")