import React from 'react';
import { Apple, Leaf, Carrot, Salad, Wheat, Trees, ArrowRight } from 'lucide-react';
import type { CategoryInfo } from '../services/api';

interface CategorySelectionProps {
  categories: Record<string, CategoryInfo>;
  selectedCategory: string | null;
  onSelectCategory: (catId: string) => void;
}

const CATEGORY_ICONS: Record<string, React.ReactNode> = {
  fruit: <Apple className="w-8 h-8 text-rose-600" />,
  fruit_leaf: <Trees className="w-8 h-8 text-emerald-600" />,
  vegetable: <Carrot className="w-8 h-8 text-amber-600" />,
  vegetable_leaf: <Salad className="w-8 h-8 text-green-600" />,
  grain: <Wheat className="w-8 h-8 text-yellow-600" />,
  grain_crop_leaf: <Leaf className="w-8 h-8 text-teal-600" />,
};

const CATEGORY_EXAMPLES: Record<string, string> = {
  fruit: 'Apples, bananas, citrus, mangoes, and harvested whole fruits.',
  fruit_leaf: 'Foliage and leaves from apple trees, grapevines, citrus orchards, etc.',
  vegetable: 'Tomatoes, potato tubers, peppers, brinjals, harvested pods.',
  vegetable_leaf: 'Leaves of tomato, potato, pepper, cucumber, and vegetable crops.',
  grain: 'Harvested rice grains, wheat kernels, maize/corn seeds, panicles.',
  grain_crop_leaf: 'Rice/paddy plants & leaves, wheat tillers, maize leaf blades.',
};

export const CategorySelection: React.FC<CategorySelectionProps> = ({
  categories,
  selectedCategory,
  onSelectCategory,
}) => {
  return (
    <div className="space-y-6">
      <div className="text-center max-w-2xl mx-auto mb-8">
        <span className="text-xs font-bold text-agri-700 uppercase tracking-wider bg-agri-100 px-3 py-1 rounded-full">
          Step 1 of 4
        </span>
        <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-2">
          Select Agricultural Category
        </h2>
        <p className="text-slate-600 mt-2 text-sm sm:text-base">
          AgriGuard AI routes images through specialized organ-level models. Select the category matching the photograph you wish to diagnose.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {Object.entries(categories).map(([catId, cat]) => {
          const isSelected = selectedCategory === catId;
          const icon = CATEGORY_ICONS[catId] || <Leaf className="w-8 h-8 text-agri-600" />;
          const exampleText = CATEGORY_EXAMPLES[catId] || cat.description;

          return (
            <div
              key={catId}
              onClick={() => onSelectCategory(catId)}
              className={`p-6 rounded-2xl cursor-pointer transition-all duration-200 border-2 relative flex flex-col justify-between ${
                isSelected
                  ? 'border-agri-600 bg-agri-50/50 shadow-md ring-2 ring-agri-500/20'
                  : 'border-slate-200 bg-white hover:border-slate-300 hover:shadow-sm'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-4">
                  <div className="w-14 h-14 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-center">
                    {icon}
                  </div>
                  <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-slate-100 text-slate-700">
                    {cat.supported_crops_count} Crops
                  </span>
                </div>

                <h3 className="text-lg font-bold text-slate-900 mb-1">{cat.display_name}</h3>
                <p className="text-xs text-slate-500 mb-3 font-medium">{cat.description}</p>
                
                <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-100">
                  <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider block mb-1">
                    What belongs here:
                  </span>
                  <p className="text-xs text-slate-700 leading-relaxed">{exampleText}</p>
                </div>
              </div>

              <div className="mt-5 pt-3 border-t border-slate-100 flex items-center justify-between text-xs font-semibold text-agri-700">
                <span>Select this category</span>
                <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
