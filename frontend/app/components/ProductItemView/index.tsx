import cn from 'classnames';
import styles from "./index.module.css";
import ProductItemViewProps from './ProductItemView.props';
import Image from 'next/image';

export default function ProductItemView({className, name, photoLink}: ProductItemViewProps) {
	return (
		<div className={cn(className, styles["product-view"])}>
			<Image className={styles.image} src={photoLink} alt="Фото товара"/>
			<span className={styles.name}>{name}</span>
		</div>
	)
}