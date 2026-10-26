import cn from 'classnames';
import styles from "./index.module.css";
import ProductViewProps from './ProductView.props';
import Image from 'next/image';

export default function ProductView({className, name, photo_link}: ProductViewProps) {
	return (
		<div className={cn(className, styles["product-view"])}>
			<Image className={styles.image} src={photo_link} alt="Фото товара"/>
			<span className={styles.name}>{name}</span>
		</div>
	)
}