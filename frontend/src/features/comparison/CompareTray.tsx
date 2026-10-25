import {Link} from 'react-router-dom';
import {ArrowRight,X} from 'lucide-react';
import {useApp} from '../../app/state';
import type {Career} from '../../shared/types';
export function CompareTray({careers}:{careers:Career[]}){const s=useApp();if(!s.selection.length)return null;return <aside className="compare-tray" aria-label="Carreras seleccionadas"><strong>{s.selection.length} de 2 carreras seleccionadas</strong><div className="selected-chips">{s.selection.map(id=><span key={id}>{careers.find(c=>c.id===id)?.name??`Carrera ${id}`}<button aria-label={`Quitar carrera ${id}`} onClick={()=>s.toggle(id)}><X size={14}/></button></span>)}</div>{s.selection.length===2?<Link className="button" to={`/comparar?a=${s.selection[0]}&b=${s.selection[1]}`}>Comparar carreras <ArrowRight size={17}/></Link>:<span className="subtle">Elige una segunda carrera</span>}</aside>}
