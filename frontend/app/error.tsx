'use client';

import { useEffect } from 'react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div>
      <h2>Что-то пошло не так</h2>
      <p>{error.message || 'Произошла непредвиденная ошибка.'}</p>
      <button onClick={() => reset()}>Попробовать снова</button>
    </div>
  );
}