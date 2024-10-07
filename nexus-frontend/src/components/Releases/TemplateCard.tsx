import { TemplateType } from '../../types/TemplateTypes';
import './TemplateCard.scss';
import DOMPurify from 'dompurify';


export interface Props {
    template: TemplateType;
    onClick: () => void;
}

export default function TemplateCard ({onClick, template}: Props) {
    return (
        <div className="release-template-view-div" onClick={onClick}>
            <div className="release-template-view-title">{template.template_name}</div>
            <div className="release-template-view-content" dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(template.template_content) }}></div>      
        </div>
    )
}