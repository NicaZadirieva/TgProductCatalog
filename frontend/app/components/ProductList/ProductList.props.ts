import ProductItem from '@/app/entities/ProductItem';
import { HtmlHTMLAttributes } from 'react';

export default interface ProductListProps extends HtmlHTMLAttributes<HTMLDivElement> {
	items: ProductItem[];
}