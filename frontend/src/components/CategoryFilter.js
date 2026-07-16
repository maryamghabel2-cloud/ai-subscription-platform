import { useState } from 'react';
import { Button } from './ui/Button';

const categories = [
  { id: 'all', name: 'همه محصولات', icon: '🌐' },
  { id: 'chat', name: 'چت و متن', icon: '💬' },
  { id: 'image', name: 'ساخت عکس', icon: '🎨' },
  { id: 'video', name: 'ساخت ویدیو', icon: '🎬' },
  { id: 'coding', name: 'کد نویسی', icon: '💻' },
  { id: 'music', name: 'موسیقی', icon: '🎵' },
  { id: 'subscription', name: 'اشتراک‌ها', icon: '📺' },
  { id: 'api', name: 'APIها', icon: '🔌' },
  { id: 'shared', name: 'اشتراکی', icon: '👥' },
];

export default function CategoryFilter({ selectedCategory, onSelect }) {
  return (
    <div className="flex flex-wrap justify-center gap-2 mb-12">
      {categories.map((category) => (
        <Button
          key={category.id}
          variant={selectedCategory === category.id ? 'primary' : 'outline'}
          size="small"
          onClick={() => onSelect(category.id)}
          className="flex items-center space-x-1"
        >
          <span>{category.icon}</span>
          <span>{category.name}</span>
        </Button>
      ))}
    </div>
  );
}
