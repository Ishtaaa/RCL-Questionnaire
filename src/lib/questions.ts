import type { Question } from './types';

export const questions: Question[] = [
  {
    id: 'fullName',
    type: 'text',
    label: 'Full name',
    required: true,
    placeholder: 'e.g. Jane Doe'
  },
  {
    id: 'age',
    type: 'number',
    label: 'Age',
    required: true
  },
  {
    id: 'hasChildren',
    type: 'radio',
    label: 'Do you have children?',
    options: ['Yes', 'No'],
    required: true
  },
  {
    id: 'cookingMethod',
    type: 'text',
    label: 'Which method did you use to cook the pocket?',
    placeholder: 'e.g. Air Fried'
  },
  {
    id: 'consumer',
    type: 'checkbox',
    label: 'Who ate the BBQ Chicken Pocket in your household?',
    options: ['Myself', 'My Kids', 'My Partner', 'Other']
  },
  {
    id: 'occasion',
    type: 'checkbox',
    label: 'What occasion(s) did you eat it for?',
    options: ['Breakfast', 'Lunch', 'Dinner', 'Snack']
  }
];
