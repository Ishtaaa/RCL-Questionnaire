export type Question =
  | {
      id: string;
      type: 'text' | 'number';
      label: string;
      required?: boolean;
      placeholder?: string;
    }
  | {
      id: string;
      type: 'radio';
      label: string;
      options: string[];
      required?: boolean;
    }
  | {
      id: string;
      type: 'checkbox';
      label: string;
      options: string[];
      required?: boolean;
    }
  | {
      id: string;
      type: 'rating';
      label: string;
      scale: number;
      required?: boolean;
    };

export type FormAnswers = Record<string, string | number | string[] | null>;
