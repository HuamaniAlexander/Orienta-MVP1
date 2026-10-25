import {expect,it,vi} from 'vitest';
import {api,mutate} from '../src/shared/api';
it('preserva un error del servidor y no presenta la solicitud como exitosa',async()=>{
 vi.stubGlobal('fetch',vi.fn().mockResolvedValue({ok:false,status:503,json:async()=>({error:{code:'database_unavailable',message:'Servicio no disponible'}})}));
 await expect(api('/carreras')).rejects.toMatchObject({status:503,code:'database_unavailable',message:'Servicio no disponible'});
});
it('obtiene CSRF antes de guardar y no expone el token en URL',async()=>{
 const fetcher=vi.fn().mockResolvedValueOnce({ok:true,status:200,json:async()=>({csrf_token:'session-bound-token'})}).mockResolvedValueOnce({ok:true,status:201,json:async()=>({id:'comparison'})});
 vi.stubGlobal('fetch',fetcher);
 await mutate('/comparaciones',{career_ids:[0,1]});
 expect(fetcher.mock.calls[0][0]).toBe('/api/v1/auth/csrf');
 expect(fetcher.mock.calls[1][1].headers['X-CSRF-Token']).toBe('session-bound-token');
 expect(fetcher.mock.calls[1][1].credentials).toBe('include');
});
