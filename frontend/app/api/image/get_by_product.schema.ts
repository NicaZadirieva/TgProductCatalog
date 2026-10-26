export interface ProductPhotoRequest {
	productId: number;
}

export interface ProductPhotoResponse {
	productId: number;
    photoLink: string;
    expiresAt: Date;
}