import { HtmlHTMLAttributes } from 'react';

export default interface ProductItemViewProps extends HtmlHTMLAttributes<HTMLDivElement> {
	productId: number;
	/**
	 * Название товара
	 */
	name: string;
	/**
	 * Ссылка на фото из MinIO
	 */
	photoLink: string;
}