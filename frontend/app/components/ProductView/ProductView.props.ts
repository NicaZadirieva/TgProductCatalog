import { HtmlHTMLAttributes } from 'react';

export default interface ProductViewProps extends HtmlHTMLAttributes<HTMLDivElement> {
	/**
	 * Название товара
	 */
	name: string;
	/**
	 * Ссылка на фото из MinIO
	 */
	photo_link: string;
}