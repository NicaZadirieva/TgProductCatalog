export interface GetByPageRequest {
	currentPage: number;
	pageSize: number;
}

export interface ProductOut {
	id: number;
    name: string;
    photoPath: string;
}
export interface GetByPageResponse {
	count: number;
	items: ProductOut[];
}

export function toProductOut(item: { id: number; name: string; photo_path: string; }): ProductOut {
	return {id: item.id, name: item.name, photoPath: item.photo_path}
}