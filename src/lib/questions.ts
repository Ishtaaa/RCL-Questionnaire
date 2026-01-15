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
  },
  {
    id: 'A_taste',
    type: 'rating',
    label: 'How much did you like the taste of BBQ Chicken Pocket A?',
    required: true,
    scale: 9,
  },
  {
    id: 'A_likes',
    type: 'text',
    label: 'What, if anything, what did you like about this BBQ Chicken Pocket A',
    required: true,
  },
  {
    id: 'A_dislikes',
    type: 'text',
    label: 'What, if anything, what did you dislike about this BBQ Chicken Pocket A',
    required: true,
  },
  {
    id: 'A_appearance',
    type: 'rating',
    label: 'How appealing was the appearance of BBQ Chicken Pocket A?',
    required: true,
    scale: 9,
  },
  {
    id: 'A_selfRelevance',
    type: 'rating',
    label: 'How relevant is BBQ Chicken Pocket A to you?',
    required: true,
    scale: 5,
  },
  {
    id: 'A_kidsRelevance',
    type: 'rating',
    label: 'How relevant is BBQ Chicken Pocket A to your kids?',
    required: false,
    scale: 5,
  },
  {
    id: 'A_expectation',
    type: 'rating',
    label: 'How well did it meet your expectations?',
    required: true,
    scale: 5,
  },
  {
    id: 'A_SelfRelevance',
    type: 'rating',
    label: 'Would you purchase this BBQ Chicken Pocket from Piemans if it was avaliable at the supermarket?',
    required: true,
    scale: 5,
  },
  {
    id: 'A_Feedback',
    type: 'text',
    label: 'Any other feedback you would like to provide on your experience with BBQ Chicken Pocket A',
    required: false,
  },
  {
    id: 'B_taste',
    type: 'rating',
    label: 'How much did you like the taste of BBQ Chicken Pocket B?',
    required: true,
    scale: 9,
  },
  {
    id: 'B_likes',
    type: 'text',
    label: 'What, if anything, what did you like about this BBQ Chicken Pocket B',
    required: true,
  },
  {
    id: 'B_dislikes',
    type: 'text',
    label: 'What, if anything, what did you dislike about this BBQ Chicken Pocket B',
    required: true,
  },
  {
    id: 'B_appearance',
    type: 'rating',
    label: 'How appealing was the appearance of BBQ Chicken Pocket B?',
    required: true,
    scale: 9,
  },
  {
    id: 'B_selfRelevance',
    type: 'rating',
    label: 'How relevant is BBQ Chicken Pocket B to you?',
    required: true,
    scale: 5,
  },
  {
    id: 'B_kidsRelevance',
    type: 'rating',
    label: 'How relevant is BBQ Chicken Pocket B to your kids?',
    required: false,
    scale: 5,
  },
  {
    id: 'B_expectation',
    type: 'rating',
    label: 'How well did it meet your expectations?',
    required: true,
    scale: 5,
  },
  {
    id: 'B_SelfRelevance',
    type: 'rating',
    label: 'Would you purchase this BBQ Chicken Pocket from Piemans if it was avaliable at the supermarket?',
    required: true,
    scale: 5,
  },
  {
    id: 'B_Feedback',
    type: 'text',
    label: 'Any other feedback you would like to provide on your experience with BBQ Chicken Pocket B',
    required: false,
  },

  
];
