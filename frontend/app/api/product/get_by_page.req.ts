import { API_URL } from '../shared/api_config';
import parseErrorMessage from '../shared/parseErrorMessage';
import RequestError from '../shared/RequestError';
import { GetByPageRequest, GetByPageResponse, toProductOut } from './get_by_page.schema';

export default async function getProductsByPage(dto: GetByPageRequest) : Promise<GetByPageResponse> {
	const res = await fetch(`${API_URL}/product?current_page=${dto.currentPage}&page_size=${dto.pageSize}`, {
        method: "GET",
        cache: "no-store",
		
    });
	if (!res.ok) {
        const message = await parseErrorMessage(res);
        throw new RequestError(message, res.status);
    }
	const data = await res.json();
	const items = data.items.map(toProductOut);
	
	return {
		items,
		count: data.count
	};
}