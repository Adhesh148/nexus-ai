export interface IssueType {
    issue_id: string;
    project_id: string;
    issue_type: string;
    summary: string;
    description?: string;
    priority?: string;
    story_points?: string;
    is_active?: boolean;
    is_staging: boolean;
    issue_url?: string;
}