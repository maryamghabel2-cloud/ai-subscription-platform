import { forwardRef } from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

const Card = forwardRef(({ 
  className, 
  children,
  hoverable = false,
  ...props 
}, ref) => {
  const baseStyles = 'bg-white rounded-xl shadow-sm border border-gray-200';
  const hoverStyles = hoverable ? 'transition-all hover:shadow-md hover:border-gray-300' : '';

  return (
    <div
      ref={ref}
      className={clsx(baseStyles, hoverStyles, className)}
      {...props}
    >
      {children}
    </div>
  );
});

Card.displayName = 'Card';

const CardHeader = forwardRef(({ className, children, ...props }, ref) => (
  <div
    ref={ref}
    className={clsx('px-6 py-4 border-b border-gray-200', className)}
    {...props}
  >
    {children}
  </div>
));

CardHeader.displayName = 'CardHeader';

const CardContent = forwardRef(({ className, children, ...props }, ref) => (
  <div
    ref={ref}
    className={clsx('p-6', className)}
    {...props}
  >
    {children}
  </div>
));

CardContent.displayName = 'CardContent';

const CardFooter = forwardRef(({ className, children, ...props }, ref) => (
  <div
    ref={ref}
    className={clsx('px-6 py-4 border-t border-gray-200 bg-gray-50 rounded-b-xl', className)}
    {...props}
  >
    {children}
  </div>
));

CardFooter.displayName = 'CardFooter';

export { Card, CardHeader, CardContent, CardFooter };
